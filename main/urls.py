from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # The home (camera) page
    path('', views.redirecting, name='home'),
    path('home/', views.home, name='home'),

    # Login page
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/login.html'), name="logout"),

    # dashboard page
    path('dashboard/', views.dashboard, name='dashboard'),

    # Logs page (Detailed info)
    path('logs/', views.log, name='log'),
    path('images/alerts/<str:imgID>/', views.getImage),
]