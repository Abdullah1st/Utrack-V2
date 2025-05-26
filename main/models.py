from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Secretary(AbstractUser):
    
    class Meta:
        db_table = 'main_secretary'
        verbose_name_plural = "Secretaries"

    def __str__(self):
        return self
