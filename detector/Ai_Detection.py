import cv2, asyncio, random, torch, os
import numpy as np
from ultralytics import YOLO
from .tracker import *
from datetime import datetime
from .Detection import * 
from .models import Student
from channels.db import database_sync_to_async

class detection:
    def __init__(self):
        
        self.tracker = Tracker()
        self.Detection = UniformDetection()
        self.people_entering = {}
        self.people_exiting ={}
        self.created_students = {}
        self.entering = set()
        self.exiting = set()
        self.hash = []
        self.prev_entering = 0
        self.prev_exiting = 0
        self.area1 = np.array([(312,388),(289,390),(474,469),(497,462)], np.int32)
        self.area2 = np.array([(279,392),(250,397),(423,477),(454,469)], np.int32)

        self.model=YOLO('detector/ML_model/yolov8s.pt')

        with open('detector/ML_model/coco1.txt', 'r') as my_file:
            self.class_list = my_file.read().split('\n')

    @database_sync_to_async
    def _create_student(self):
        return Student.objects.create(is_student=True)

    async def main(self, frame):

        frame=cv2.resize(frame,(1020,500))
        results=self.model.predict(frame)
        a=results[0].boxes.data.cpu().numpy()
        px=a.astype("float")
        list=[]
        
                
        for row in px:
            x1=int(row[0])
            y1=int(row[1])
            x2=int(row[2])
            y2=int(row[3])
            d=int(row[5])
            c=self.class_list[d]
           
            if 'person' in c:
                list.append([x1,y1,x2,y2])
                
        bbox_id = self.tracker.update(list)
        for bbox in bbox_id:
            x3,y3,x4,y4,id = bbox
            
            results1 = cv2.pointPolygonTest(self.area2, (x4,y4), False)
            if results1 >=0:
                self.people_entering[id] = (x4,y4)
                
            if id in self.people_entering:
                results2 = cv2.pointPolygonTest(self.area1, (x4,y4), False)

                if (results2>=0) and (id not in self.created_students):
                    student = await self._create_student()
                    self.created_students[id] = student  # Store the student object
                    print(f"Created new student ID: {student.id} for tracking ID {id}")
                    person_crop = frame[y3:y4, x3:x4]
                    output_folder = "ai_images"
                    id_image = int(''.join(str(random.randint(0, 9)) for _ in range(7)))
                    
                    cropped_image_path = os.path.join(output_folder, f"{id_image}.jpg")
                    cv2.imwrite(cropped_image_path, person_crop)
                    
                    print(f" Cropped image saved: {cropped_image_path}")
                    await self.Detection.detect(id_image,id)
                    self.entering.add(id)
                    self.Detection.remove_image("ai_images")

            results3 = cv2.pointPolygonTest(self.area1, (x4,y4), False)
            if results3 >=0:
                self.people_exiting[id] = (x4,y4)
                cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
                
            if id in self.people_exiting:
                results4 = cv2.pointPolygonTest(self.area2,(x4,y4),False)
                if results4>=0:
                    self.exiting.add(id)
                    

        print(f"number of violation is {len(self.Detection.alert)}")
        

        self.prev_entering = len(self.entering)
        print(self.prev_entering)
        self.prev_exiting = len(self.exiting)