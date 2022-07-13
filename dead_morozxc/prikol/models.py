from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Userinfo(models.Model):
	user = models.OneToOneField(User, default=None, null = True, blank=True, on_delete = models.CASCADE)
	chat_id = models.CharField(max_length = 255, default=None,blank = True, null = True)
	current_command = models.CharField(max_length = 255, default=None,blank = True, null = True)
	pocket = models.FloatField(blank = True, null = True, default = None)
	create_date = models.DateTimeField(default=timezone.now)
	user_task = models.OneToOneField("UserTask", default=None, null = True, blank=True, on_delete = models.SET_DEFAULT)


class UserImage(models.Model):
	screenshot = models.ImageField(upload_to = "images/", blank = True, null = True, default = None)
	userI = models.ForeignKey("Userinfo", default=None, null = True, blank=True, on_delete = models.SET_DEFAULT)
	create_date = models.DateTimeField(default=timezone.now)

class UserTask(models.Model):
	status = models.CharField(max_length = 15, default=None, blank = True, null = True)
	task_id = models.CharField(max_length = 255, default=None, blank = True, null = True)
	link = models.CharField(max_length = 255, default=None, blank = True, null = True)
	social_network = models.CharField(max_length = 255, default=None, blank = True, null = True)
	action = models.CharField(max_length = 500, default=None, blank = True, null = True)
	reward = models.FloatField(blank = True, null = True, default = None)
	comment_id = models.CharField(max_length = 255, default=None, blank = True, null = True)
	comment_text = models.CharField(max_length = 255, default=None, blank = True, null = True)
	comment_username = models.CharField(max_length = 255, default=None, blank = True, null = True)
	comment = models.CharField(max_length = 255, default=None, blank = True, null = True)
	create_date = models.DateTimeField(default=timezone.now)