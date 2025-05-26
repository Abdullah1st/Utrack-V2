from django.db import models


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    is_student = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Student_id {self.id}"
    class Meta:
        ordering = ['-id'] 
        get_latest_by = 'date'


class Leaving(models.Model):
    leaving = models.IntegerField(default=0)
    class Meta:
        db_table = 'detector_Leaving'
        verbose_name_plural = "Leavings"


class Violation(models.Model):
    student = models.ForeignKey(
        Student,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='violations'
    )
    secretary = models.ForeignKey(
        'main.Secretary',
        null=True,
        blank=True,
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