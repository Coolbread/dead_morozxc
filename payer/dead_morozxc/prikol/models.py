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
	count_tasks = models.IntegerField(blank = True, null = True, default = 0)
	create_date = models.DateTimeField(default=timezone.now)
	lang_code = models.CharField(max_length = 2, default=None,blank = True, null = True)
	force_check = models.BooleanField(default = False ,blank = True)


class UserImage(models.Model):
	userI = models.ForeignKey("Userinfo", default=None, null = True, blank=True, on_delete = models.SET_DEFAULT)
	screenshot = models.ImageField(upload_to = "images/", blank = True, null = True, default = None)
	create_date = models.DateTimeField(default=timezone.now)

class UserTask(models.Model):
	userI = models.ForeignKey("Userinfo", default=None, null = True, blank=True, on_delete = models.SET_DEFAULT)
	userImage = models.OneToOneField("UserImage", default=None, null = True, blank=True, on_delete = models.SET_DEFAULT)
	status = models.CharField(max_length = 15, default=None, blank = True, null = True)
	#Статус будет иметь значения: Done - задание сделано, Skipped - задание было пропущено(неважно с помощью какой кнопки)
	#Given - задание в процессе выполнения
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
