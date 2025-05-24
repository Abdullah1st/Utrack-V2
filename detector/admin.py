from django.contrib import admin
from .models import Violation,Dashboard, Student

# Register your models here.


class DashboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_count', 'violation_count', 'date')

class ViolationAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'isNotified', 'image', 'date')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_student', 'date')


admin.site.register(Violation, ViolationAdmin)
admin.site.register(Dashboard, DashboardAdmin)
admin.site.register(Student, StudentAdmin)