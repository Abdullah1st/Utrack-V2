from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("Violation/", views.view_Violation, name="view_Violation"),
    # path('dashboard/', views.dashboard_view, name='dashboard-list'),
    
    path('api/dashboard/all/<str:type>/', views.DashboardListView.as_view(), name='dashboard-list'),
    path('api/dashboard/today/', views.TodayListView.as_view(), name='todayDash'),
    path('api/violations/all/', views.ViolationListView.as_view(), name='Violation-list'),

   
]

