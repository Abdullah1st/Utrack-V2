from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Secretary
# Register your models here.

@admin.register(Secretary)
class SecretaryAdmin(UserAdmin):
    list_display = ('id', 'username', 'is_staff', 'is_superuser')
