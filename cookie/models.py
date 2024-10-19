from django.db import models

# Create your models here.

class Task(models.Model):
    TASK_STATES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(max_length=20, choices=TASK_STATES, default='PENDING')
    time_needed = models.IntegerField()  # Dakika cinsinden süre
    prerequisite = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_task')

    def __str__(self):
        return self.name
