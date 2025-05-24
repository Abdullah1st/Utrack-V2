from ultralytics import YOLO
from datetime import datetime
import os
from django.utils import timezone
from django.http import JsonResponse
from .models import Violation
from django.conf import settings
from django.core.files import File


class UniformDetection:
    def __init__(self, model_path="detector/ML_model/best1.pt"):
        """Initialize the YOLO model for uniform detection."""
        self.model = YOLO(model_path)
        self.alert = set()

    def remove_image(self, path):
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
        for filename in os.listdir(path):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                file_path = os.path.join(path, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


    def detect(self, id_image, id):
        results = self.model(f"ai_images/violator{id_image}.png")
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
            cropped_path = os.path.join(settings.BASE_DIR, 'ai_images', f'violator{id_image}.png')
            print(f"Alert! Unknown class detected for ID {id}")
            
            # Create and save the violation
            violation = Violation()
            with open(cropped_path, 'rb') as f:
                violation.image.save(f'violator{id_image}.png', File(f), save=True)