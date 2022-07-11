import telebot
from telebot import types
from django.conf import settings
from .models import User_info
from .models import User_Image
from PIL import Image
from io import BytesIO
#from .models import Team
from django.contrib.auth.models import User
import psycopg2
import time
from .menus import get_menu

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

		self.user_info = User_info.objects.get(user = self.u)
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
	
	def pay(self):
		self.user_info.pocket += 10
		self.user_info.save()



@bot.message_handler(commands=['start'])
def greetings(message):
	user_ID = User_info.objects.filter(chat_id = str(message.chat.id))
	if len(user_ID) == 0:
		bot.send_message(message.chat.id, "Здарова")
		user = User.objects.create_user(username = "p" + str(message.chat.id), password = None)
		user_info = User_info.objects.create(user = user,
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

	user_info = User_info.objects.get(user = u)
	if user_info.current_command == "process_get_screen":
		user_info.current_command = ""
		user_info.save()
		file_info = bot.get_file(message.photo[0].file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		stream = BytesIO(downloaded_file)
		im = Image.open(stream)
		img = User_Image.objects.create(screenshot = im,
			user_i = user_info)
		bot.send_message(message.chat.id, im)
		#user_info.screenshot = bot.download_file(file_info_1.file_path)
		#src = ""
		#bot.send_message(message.chat.id, src)
		#with open(src, 'wb') as new_file:
		#	new_file.write(downloaded_file)

	else:
		bot.send_message(message.chat.id, "Чувак, зачем мне твой скрин? Нажми на кнопку <b> Задание выполнено </b> и только потом присылай подтверждение!")