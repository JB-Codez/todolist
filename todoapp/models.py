from django.conf import settings
from django.db import models
from django.apps import apps # https://stackoverflow.com/a/43847288


# Create your models here.
class ToDoItem(models.Model):
    #task_author = models.ForeignKey('todologin.DashboardUser',on_delete=models.CASCADE) #https://stackoverflow.com/a/43847288
    #https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#referencing-the-user-model
    task_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) # https://stackoverflow.com/a/40954392
    task_description = models.CharField(max_length=50)
    task_complete = models.BooleanField(default=False)
    task_created = models.DateTimeField(auto_now_add=True)
    task_is_private = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return self.task_description
    