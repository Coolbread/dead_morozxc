from django.db import models

from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class User_info(models.Model):
	user = models.OneToOneField(User, default=None, null = True, blank=True, on_delete = models.CASCADE)
	chat_id = models.CharField(max_length = 255, default=None,blank = True, null = True)
	current_command = models.CharField(max_length = 255, default=None,blank = True, null = True)
	pocket = models.IntegerField(blank = True, null = True, default = None)

class User_Image(models.Model):
	screenshot = models.ImageField(upload_to = "images/", blank = True)
	user_i = models.ForeignKey("User_info", default=None, null = True, blank=True, on_delete = models.CASCADE)