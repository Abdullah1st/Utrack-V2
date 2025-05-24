from django.db import models

class Violation(models.Model):
    id = models.AutoField(primary_key=True)   
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


class Dashboard(models.Model):
    id = models.AutoField(primary_key=True) 
    student_count = models.IntegerField()
    violation_count = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id'] 
        get_latest_by = 'date'

    def __str__(self):
        return f"Count: {self.student_count} - on {self.date.strftime('%Y-%m-%d %H:%M:%S')} - Violations: {self.violation_count}"
    

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    is_student = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id'] 
        get_latest_by = 'date'

    
