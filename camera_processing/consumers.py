import asyncio, json, cv2, websockets
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .camera import VideoCamera
from detector.Ai_Detection import detection
from detector.models import Violation, Student
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class FrameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('frameGroup', self.channel_name)
        await self.accept()
        
        if not hasattr(FrameConsumer, 'camera'):
            FrameConsumer.camera = VideoCamera()
            await asyncio.sleep(0.5)
            asyncio.create_task(FrameConsumer.send_frames(self))
            print('Creating new camera instance')
        else:
            # print(self.camera.video)
            print('Using existing camera instance')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('frameGroup', self.channel_name)
        await super().disconnect(close_code)

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_frames(self):
        try:
            # await websockets.connect(f'ws://{self.scope['headers'][0][1].decode('utf-8')}/ws/modelFrames/')
            while True:
                await self.channel_layer.group_send(
                    'frameGroup',
                    {
                        'type': 'frame.handler',
                        'frame': await self.camera.get_frame().__anext__()
                    }
                )
        except Exception as s:
            print(f'Error in send_frames(), line 39\n{s}')
            del FrameConsumer.camera
    async def frame_handler(self, event):
        await self.send(bytes_data=event['frame'])



class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('dashGroup', self.channel_name)
        await self.accept()
        self.exec = ThreadPoolExecutor()
        self.loop = asyncio.get_event_loop()
        self.vioTable = Violation.objects
        self.stTable = Student.objects
        asyncio.create_task(self.sendAlert())
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('dashGroup', self.channel_name)
        await super().disconnect(close_code)

    async def receive(self, text_data):
        data:dict = json.loads(text_data)
        if 'acknowledgement' in data:
            await self.loop.run_in_executor(self.exec, lambda: self.vioTable.filter(id=data['acknowledgement']).update(isNotified=True))
        else:
            print(data['rmNotification'])
            violatorID, isConfirmed = data['rmNotification']['violatorID'], data['rmNotification']['isConfirmed']
            if isConfirmed:
                await self.loop.run_in_executor(self.exec, lambda: self.vioTable.filter(id=violatorID).update(state='confirmed'))
            else:
                await self.loop.run_in_executor(self.exec, lambda: self.vioTable.filter(id=violatorID).update(state='ignored'))
                await self.loop.run_in_executor(self.exec, lambda: self.stTable.order_by('id').first().delete())


    async def sendAlert(self):
        try:
            violations:list = await self.loop.run_in_executor(self.exec, lambda: list(self.vioTable.filter(state='pending')))
            for violation in violations:
                await self.channel_layer.group_send(
                    'dashGroup',
                    {
                        'type': 'dashHandler',
                        'data': {
                            'notification': {
                                'id': f'{violation.id}',
                                'imageID': f'{str(violation.image)[7:]}',
                                'date': f'{str(violation.date)[:19]}'
                            }
                        }
                    }
                )
            currentTime = datetime.now().timestamp()
            while True:
                await asyncio.sleep(0.3)
                violator:list = await self.loop.run_in_executor(self.exec, lambda: list(self.vioTable.filter(state='pending', isNotified=False)))
                if violator and currentTime < violator[0].date.timestamp():
                    await self.channel_layer.group_send(
                        'dashGroup',
                        {
                            'type': 'dashHandler',
                            'data': {
                                'violator': {
                                    'id': f'{violator[0].id}',
                                    'imageID': f'{str(violator[0].image)[7:]}',
                                    'date': f'{str(violator[0].date)[:19]}'
                                }
                            }
                        }
                    )
        except Exception as e:
            print(e)

    async def dashHandler(self, event):

        json.dumps(event['data'])
        await self.send(text_data=json.dumps(event['data']))


class AiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('frameGroup', self.channel_name)
        await self.accept()
        self.detector = detection()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('frameGroup', self.channel_name)
        await super().disconnect(close_code)

    async def frame_handler(self, event):
        await asyncio.to_thread(self.detector.main, self.convert_bytes_to_frame(event['frame']))
        # await self.detector.main(self.convert_bytes_to_frame(event['frame']))
    
    def convert_bytes_to_frame(self, frame_bytes):
        return cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)