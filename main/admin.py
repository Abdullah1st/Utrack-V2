from django.contrib import admin
from .models import Secretary
# Register your models here.


class SecretaryAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')


admin.site.register(Secretary, SecretaryAdmin)