from django.db import models


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    is_student = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id'] 
        get_latest_by = 'date'


class Violation(models.Model):
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='violations'
    )
    secretary_id = models.ForeignKey(
        'main.Secretary',
        on_delete=models.CASCADE,
        related_name='violations'
    )
    image = models.ImageField(upload_to='alerts')  
    date = models.DateTimeField(auto_now_add=True)  
    
    STATE_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('ignored', 'Ignored'),
        ('pending', 'Pending'),
    ]

    state = models.CharField(
        max_length=10,
        choices=STATE_CHOICES,
        default='pending',
    )

    isNotified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id'] 
        get_latest_by = 'date'

    def __str__(self):
        return f"ID: {self.id}, state: {self.state}"