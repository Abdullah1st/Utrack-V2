from ultralytics import YOLO
from datetime import datetime
import os, asyncio
from django.utils import timezone
from django.http import JsonResponse
from .models import Violation, Student
from main.models import Secretary
from django.conf import settings
from django.core.files import File
from channels.db import database_sync_to_async


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
    def _create_violation(self, violation, cropped_path, id_image):
        with open(cropped_path, 'rb') as f:
            violation.image.save(f'{id_image}.jpg', File(f), save=True)
        return violation 

    async def detect(self, id_image, id):
        results = self.model(f"ai_images/{id_image}.jpg")
        if results[0].boxes is None or len(results[0].boxes) == 0:
            print(f"⚠ No detection found.")
            return None

        if id in self.alert:
            print(f"ID {id} is detected before")
            return

        box = results[0].boxes[0]
        class_id = int(box.cls[0].cpu().numpy())
        class_name = self.model.names[class_id]

        if class_name == "person_without_thobe_shemagh":
            self.alert.add(id)
            cropped_path = os.path.join(settings.BASE_DIR, 'ai_images', f'{id_image}.jpg')
            print(f"Alert! Unknown class detected for ID {id}")
            
            secretary, student = await asyncio.gather(
                self._get_secretary(),
                self._get_student()
            )
            # Create and save the violation
            violation = Violation(
                secretary=secretary,
                student=student
            )
            await self._create_violation(violation, cropped_path, id_image)