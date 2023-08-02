from django.db import models

# Create your models here.
class ToDoItem(models.Model):
    task_description = models.CharField(max_length=50)
    task_complete = models.BooleanField(default=False)
    task_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.task_description
    