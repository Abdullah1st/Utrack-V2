from rest_framework import serializers
from .models import Dashboard, Violation, Student


class DashboardSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Dashboard
        fields = ['student_count','violation_count','date']


class StudentSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Student
        fields = ['id','is_student','date']


class ViolationSerializer(serializers.ModelSerializer):
    state_display = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = Violation
        fields = ['id','state', 'state_display','image', 'date']
    
    def get_state_display(self, obj):
        return obj.get_state_display()