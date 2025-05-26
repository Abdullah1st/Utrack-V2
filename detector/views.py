from django.shortcuts import render
from django.http import StreamingHttpResponse

import cv2
from datetime import datetime, time, timedelta
from django.utils import timezone

from .Ai_Detection import detection

from .models import Violation, Student

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ViolationSerializer, StudentSerializer

# Create your views here.
def index(request):
    stream()
    return render(request,"index.html")

def stream():
    ai_object = detection()
    cap = cv2.VideoCapture('main/static/vids/videopeople.mp4')
    
    if not cap.isOpened():
        print("Failed to open video file")
        return

    try:
        while True:
            ret, frame = cap.read()
            ai_object.main(frame)
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

# def video_feed(request):
#     return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')

class DashboardListView(APIView):
    def get(self, request, type):
        all_students = Student.objects.all()
        all_violations = Violation.objects.all()
        if type == 'int':
            return Response({'students': all_students.count(), 'violations': all_violations.count()})
        elif type == 'obj':
            students = StudentSerializer(all_students.order_by('-date'), many=True)
            violations = ViolationSerializer(all_violations.order_by('-date'), many=True)
            return Response({'student_objects':students.data, 'violation_objects':violations.data})

        return Response({'Endpoints Available':['int', 'obj']})

class TodayListView(APIView):
    def get(self, request):
        now = timezone.now()
        today = now.date()
        today_6am = timezone.make_aware(datetime.combine(today, time(6, 0)))
        todayStudents = Student.objects.filter(
            date__gte=today_6am,
        ).count()

        todayViolations = Violation.objects.filter(
            date__gte=today_6am,
            state='confirmed'
        ).count()
        return Response({'studentsCount': todayStudents, 'violationsCount': todayViolations, 'todayDate': today.strftime('%A %b %d')})

    
class ViolationListView(APIView):
    def get(self, request):
        all_violations = Violation.objects.all()
        serializer = ViolationSerializer(all_violations, many=True)
        return Response(serializer.data)

