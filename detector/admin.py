from django.contrib import admin
from .models import Violation, Student

# Register your models here.

class ViolationAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'student', 'secretary', 'image', 'date')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_student', 'date')


admin.site.register(Violation, ViolationAdmin)
admin.site.register(Student, StudentAdmin)