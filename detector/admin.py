from django.contrib import admin
from .models import Violation, Student, Leaving

# Register your models here.

class ViolationAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'student', 'secretary', 'image', 'date')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_student', 'date')

class LeavingAdmin(admin.ModelAdmin):
    list_display = ('id', 'leaving')

admin.site.register(Violation, ViolationAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Leaving, LeavingAdmin)