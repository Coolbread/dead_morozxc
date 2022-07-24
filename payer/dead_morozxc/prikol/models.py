from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Userinfo(models.Model):
	user = models.OneToOneField(User, default=None, null = True, blank=True, on_delete = models.CASCADE)
	chat_id = models.CharField(max_length = 255, default=None,blank = True, null = True)
	current_command = models.CharField(max_length = 255, default=None,blank = True, null = True)
	prev_func = models.CharField(max_length = 255, default=None,blank = True, null = True)
	pocket = models.FloatField(blank = True, null = True, default = None)
	count_tasks = models.IntegerField(blank = True, null = True, default = 0)
	create_date = models.DateTimeField(default=timezone.now)
	lang_code = models.CharField(max_length = 2, default=None,blank = True, null = True)
	force_check = models.BooleanField(default = False ,blank = True)
	pocket_id = models.CharField(max_length = 255, default=None,blank = True, null = True)
	withdrawal_method = models.CharField(max_length = 32, default=None,blank = True, null = True)
	name_category = models.CharField(max_length = 255, default=None,blank = True, null = True)

class UserImage(models.Model):
	userI = models.ForeignKey("Userinfo", default=None, null = True, blank=True, on_delete = models.SET_DEFAULT)
	screenshot = models.ImageField(upload_to = "images/", blank = True, null = True, default = None)
	create_date = models.DateTimeField(default=timezone.now)

class UserTask(models.Model):
	userI = models.ForeignKey("Userinfo", default=None, null = True, blank=True, on_delete = models.SET_DEFAULT)
	userImage = models.OneToOneField("UserImage", default=None, null = True, blank=True, on_delete = models.SET_DEFAULT)
	category = models.ForeignKey("TaskCategory", default = None, null = True, blank = True, on_delete = models.SET_DEFAULT)
	account = models.ForeignKey("Accounts", default = None, null = True, blank = True, on_delete = models.SET_DEFAULT)
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

class TaskCategory(models.Model):
	ru_name = models.CharField(max_length = 255, default=None, blank = True, null = True)
	en_name = models.CharField(max_length = 255, default=None, blank = True, null = True)
	need_account = models.BooleanField()
	category_id = models.CharField(max_length = 20, default = None, blank = True, null = True) 

class Accounts(models.Model):
	userI = models.ForeignKey("Userinfo", default=None, null = True, blank=True, on_delete = models.SET_DEFAULT)
	account_name = models.CharField(max_length = 256, blank = True, null = True, default = None)
	creation_date = models.DateTimeField(default = timezone.now)

class WithdrawalMethods(models.Model):
	name = models.CharField(max_length = 32)
	min_withdrawal = models.IntegerField()
	speed = models.CharField(max_length = 16)
	regex = models.CharField(max_length = 256, blank = True, null = True, default = None)
	example = models.CharField(max_length = 256, blank = True, null = True, default = None)
	is_active = models.BooleanField(default = True)

	def unicode(self):
		return self.name + " " + str(self.min_withdrawal) + " " + self.speed

class Withdrawal(models.Model):
	user = models.ForeignKey(Userinfo, null = True, on_delete = models.SET_NULL)
	method = models.ForeignKey(WithdrawalMethods, null = True, on_delete = models.SET_NULL)

	outcome = models.FloatField(null = True, blank = True, default = None)
	rub_outcome = models.FloatField(null = True, blank = True, default = None)
	currency = models.CharField(max_length = 10, default = "USD")

	creation_date = models.DateTimeField(default = timezone.now)
	confirmation_date  = models.DateTimeField(null = True, blank = True, default = None)

	status = models.CharField(max_length = 120, default = "New")
	payment_method = models.CharField(max_length = 60, default = "Crypto")

	wallet_info = models.CharField(max_length = 4096, null = True, blank = True, default = None)

	payout_id = models.CharField(max_length = 128, null = True, blank = True, default = None)

	is_take_into_account = models.BooleanField(default = False)
