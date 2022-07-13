import telebot
from telebot import types
from django.conf import settings
from .models import Userinfo
from .models import UserImage
from .models import UserTask
from PIL import Image
from io import BytesIO
from django.core.files.images import ImageFile
#from .models import Team
from django.contrib.auth.models import User
import psycopg2
import time

from .menus import get_menu
from .messages import get_message

bot = telebot.TeleBot(settings.DEAD_MOROZXC_TOKEN, threaded = False)
bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://langlibclub.com/dead_morozxc/bot/process-new-updates/")

class TelegramCommand():
	def get_command(self,command):
		commands_list = [
		#{"text" : "Получить новое задание", "function" : },
		{"text" : "Задание выполнено", "function" : self.get_screen},
		{"text" : "/start", "function" : self.greetings},
		{"text" : "/main_menu", "function" : self.greetings},
		{"text" : "Дай задание", "function" : self.give_task},
		]

		for c in commands_list:
			if c["text"] == command:
				return c


	def __init__(self, message):
		try:
			self.u = User.objects.get(username = "p" + str(message.chat.id))
		except:
			self.user_info = None
			self.command = False
			return

		self.user_info = Userinfo.objects.get(user = self.u)
		self.user_t = self.user_info.user_task
		self.message = message
		self.content = message.text
		if self.user_info.current_command:
			self.command = self.get_command(self.user_info.current_command)
		else:
			self.command = self.get_command(self.content)

	def execute(self):
		#if (self.content == get_message("back_button", self.lang_code)): 
		#	self.command = self.get_command(self.additional_user_info.prev_func, "en")
		#	self.command = self.get_command(self.command["back_function"], "en")

		r = self.command["function"](self.message)
		return r

	def greetings(self, message):
		response = {}
		response["menu"] = get_menu("main_menu")
		response["text"] = "<b>Пора выполнять задания!</b>"
		return response

	def get_screen(self,message):
		self.user_info.current_command = "process_get_screen"
		self.user_info.save()
		response = {}
		response["text"] = "<b>Кидай скриншот выполненного задания и награда твоя</b>"
		return response
	
	def give_task(self,message):
		response = {}
		t = {
			"status" : "Given",
			"task_id" : "1",
			"link" : "https://suda/nado/pereyti",
			"social_network" : "ChinChopa",
			"action" : "Поцелуй свою маму",
			"reward" : 777.777,
			"comment" : "Не надо ниче писать!!!",
		}
		user_t = UserTask.objects.create(status = t["status"],
			task_id = t["task_id"],
			link = t["link"],
			social_network = t["social_network"],
			action = t["action"],
			reward = t["reward"],
			comment = t["comment"])
		self.user_info.user_task = user_t
		self.user_info.save()

		if user_t.status == "No tasks":
			response["text"] = get_message("no_task_message")
		else:
			response["text"] = get_message("task_message", t)

		response["menu"] = get_menu("task_menu")
		return response

	def pay(self):
		self.user_info.pocket += 10
		self.user_info.save()



@bot.message_handler(commands=['start'])
def greetings(message):
	user_ID = Userinfo.objects.filter(chat_id = str(message.chat.id))
	if len(user_ID) == 0:
		bot.send_message(message.chat.id, "Здарова")
		user = User.objects.create_user(username = "p" + str(message.chat.id), password = None)
		user_info = Userinfo.objects.create(user = user,
			chat_id = message.from_user.id,
			current_command = "",
			pocket = 0)
	else:
		command = TelegramCommand(message)
		response = command.execute()
		if ("menu" in response):
			# Create keyboard
			keyboard = telebot.types.ReplyKeyboardMarkup()
			for m in response["menu"]:
				keyboard.row(*m)
		else:
			keyboard = None
		if ("disable_web_preview" in response):
			disable_web_preview = response["disable_web_preview"]
		else:
			disable_web_preview = None
		if ("parse_mode" in response):
			parse_mode = response["parse_mode"]
		else:
			parse_mode = 'HTML'
		bot.send_message(message.chat.id,
		response["text"],
		reply_markup = keyboard,
		parse_mode = parse_mode,
		disable_web_page_preview = disable_web_preview)


@bot.message_handler(content_types=["text"])
def procces_message(message):
	command = TelegramCommand(message)
	response = command.execute()
	if ("menu" in response):
		# Create keyboard
		keyboard = telebot.types.ReplyKeyboardMarkup()
		for m in response["menu"]:
			keyboard.row(*m)
	else:
		keyboard = None
	if ("disable_web_preview" in response):
		disable_web_preview = response["disable_web_preview"]
	else:
		disable_web_preview = None
	if ("parse_mode" in response):
		parse_mode = response["parse_mode"]
	else:
		parse_mode = 'HTML'
	bot.send_message(message.chat.id,
	response["text"],
	reply_markup = keyboard,
	parse_mode = parse_mode,
	disable_web_page_preview = disable_web_preview)

@bot.message_handler(content_types=["photo"])
def get_screen(message):
	try:
		u = User.objects.get(username = "p" + str(message.chat.id))
	except:
		bot.send_message(message.chat.id, "Чувак, сначала введи /start !")
		return

	user_info = Userinfo.objects.get(user = u)
	if user_info.current_command == "process_get_screen":
		user_info.current_command = ""
		user_info.user_task.status = "Done"
		user_info.save()
		file_info = bot.get_file(message.photo[0].file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		im = ImageFile(BytesIO(downloaded_file), name = user_info.chat_id + '.jpg')
		img = UserImage.objects.create(userI = user_info, screenshot = im)

	else:
		bot.send_message(message.chat.id, "Чувак, зачем мне твой скрин? Нажми на кнопку"+"<b> Задание выполнено </b>" + "и только потом присылай подтверждение!")