import cv2, asyncio
from concurrent.futures import ThreadPoolExecutor
import numpy as np


class VideoCamera(object):
    def __init__(self):
        # url = 'rtsp://abdullah:@192.168.100.100:8081/h264_ulaw.sdp'
        # 'http://192.168.100.100:4747/video'
        # 'main/static/vids/videopeople.mp4'
        self.video = cv2.VideoCapture('main/static/vids/videopeople.mp4')
        self.counter:int = 0
        self.dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        _, self.dummy_jpeg = cv2.imencode('.jpg', self.dummy_frame)
        if not self.video.isOpened():
            raise ValueError('Could not open frames source')
    
    def __del__(self):      # Camera Shut-Down
        self.video.release()

    def read_frame(self):   # Frame reader
        _, frame = self.video.read()
        # if not ret and self.counter <= 8000:
        #     self.counter += 1
        #     return self.dummy_jpeg.tobytes()
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    
    async def get_frame(self):
        yield await asyncio.get_event_loop().run_in_executor(ThreadPoolExecutor(), self.read_frame)