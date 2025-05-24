from django.urls import path
from .consumers import FrameConsumer, DashboardConsumer, AiConsumer

ws_urlpatterns = [
    path('ws/clientFrames/', FrameConsumer.as_asgi()),
    path('ws/modelFrames/', AiConsumer.as_asgi()),
    path('ws/dashFrames/', DashboardConsumer.as_asgi()),
]
