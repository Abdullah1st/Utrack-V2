from ultralytics import YOLO
from datetime import datetime
import os, asyncio, cv2
from django.utils import timezone
from django.http import JsonResponse
from .models import Violation, Student
from main.models import Secretary
from django.conf import settings
from django.core.files import File
from channels.db import database_sync_to_async
import numpy as np

class UniformDetection:
    def __init__(self, model_path="detector/ML_model/best1.pt"):
        """Initialize the YOLO model for uniform detection."""
        self.model = YOLO(model_path)
        self.alert = set()

    def remove_image(self, path):
        try:
            os.remove(f'{path}/{os.listdir(path)[0]}')
            print(f"done deleting ai_images file")
        except Exception as e:
            print(f"Error deleting ai_images file: {e}")

    @database_sync_to_async
    def _get_secretary(self):
        return Secretary.objects.order_by('-last_login').first()

    @database_sync_to_async
    def _get_student(self):
        return Student.objects.first()

    @database_sync_to_async
    def _create_violation(self, violation, image_data, id_image):
        from io import BytesIO
        from django.core.files.uploadedfile import InMemoryUploadedFile

        img_io = BytesIO(image_data)
        image_file = InMemoryUploadedFile(
            file=img_io,
            field_name='image',
            name=f'{id_image}.jpg',
            content_type='image/jpeg',
            size=len(image_data),
            charset=None
        )

        # Save violation with image
        violation.image.save(f'{id_image}.jpg', image_file, save=True)
        return violation 

    async def detect(self, id_image, id, image_data):
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        results = self.model(img)

        if not results[0].boxes:
            return

        box = results[0].boxes[0]
        class_name = self.model.names[int(box.cls[0])]

        if class_name == "person_without_thobe_shemagh":
            secretary, student = await asyncio.gather(
                self._get_secretary(),
                self._get_student()
            )
            # Create and save the violation
            violation = Violation(
                secretary=secretary,
                student=student
            )
            await self._create_violation(violation, image_data, id_image)