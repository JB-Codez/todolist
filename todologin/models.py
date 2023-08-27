
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class DashboardUser(AbstractUser):
    user_image = models.ImageField(null=True, blank=True, upload_to="profile_pics/", default="profile_pics/no_prof_pic.PNG")
    
    def __str__(self):
        return self.username