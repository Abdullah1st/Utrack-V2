from django.urls import path
from . import views


urlpatterns = [
    # The home (camera) page
    path('', views.redirecting, name='home'),
    path('home/', views.home, name='home'),
    # path('alertClient/', views.alertStream, name='alertClient'),
    # path('pushAlert/', views.pushAlert, name='pushAlert'),

    # Login page
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    # Statistics and analysis page
    path('dashboard/', views.dashboard, name='dashboard'),

    # Logs page (Detailed info)
    path('logs/', views.log, name='log'),
    path('images/alerts/violator<str:imgID>.png/', views.getImage),
]