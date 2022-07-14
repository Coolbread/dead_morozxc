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
	def get_command(self,command, lang_code):
		commands_list = [
		#{"text" : "Получить новое задание", "function" : },
		{"ru" : "Wait for language", "en" : "Wait for language", "function" : self.process_language},
		{"ru" : "process_get_screen", "en" : "process_get_screen", "function" : self.process_get_screen},
		{"ru" : "Получить награду", "en" : "Get reward", "function" : self.pay},
		{"ru" : "Задание выполнено", "en" : "Job is done" , "function" : self.get_screen},
		{"ru" : "/start", "en" : "/start", "function" : self.greetings},
		{"ru" : "/main_menu","en" : "/main_menu", "function" : self.greetings},
		{"ru" : "Дай задание", "en" : "Give me task", "function" : self.give_task},
		]

		for c in commands_list:
			if c[lang_code] == command:
				return c


	def __init__(self, message):
		try:
			self.u = User.objects.get(username = "p" + str(message.chat.id))
		except:
			self.user_info = None
			self.command = False
			return

		self.user_info = Userinfo.objects.get(user = self.u)
		try:
			self.user_task = UserTask.objects.get(userI = self.user_info, status = "Given")
		except:
			self.user_task = None
		self.message = message
		self.lang_code = self.user_info.lang_code
		self.content = message.text
		if self.user_info.current_command:
			self.command = self.get_command(self.user_info.current_command, self.lang_code)
		else:
			self.command = self.get_command(self.content, self.lang_code)

	def execute(self):
		#if (self.content == get_message("back_button", self.lang_code)): 
		#	self.command = self.get_command(self.additional_user_info.prev_func, "en")
		#	self.command = self.get_command(self.command["back_function"], "en")

		r = self.command["function"](self.message)
		return r
	
	def process_language(self, message):
		# Check if language set correctly 
		if (self.content == "Русский"):
			self.lang_code = "ru"
			self.user_info.current_command = None
			self.user_info.lang_code = "ru"
			self.user_info.save()
		elif (self.content == "English"):
			self.lang_code = "en"
			self.user_info.current_command = None
			self.user_info.lang_code = "en"
			self.user_info.save()
		else:
			response = {}
			response["text"] = get_message("wrong_language", "en")
			response["menu"] = get_menu("language_menu", "en")
			return response
	
	def greetings(self, message):
		response = {}
		response["menu"] = get_menu("main_menu", self.lang_code)
		if self.lang_code == "ru":
			response["text"] = "<b>Пора выполнять задания!</b>"
		else:
			response["text"] = "<b>It's time to complete the tasks!</b>"
		return response

	def get_screen(self,message):
		self.user_info.current_command = "process_get_screen"
		self.user_info.save()
		response = {}
		if self.lang_code == "ru":
			response["text"] = "<b>Кидай скриншот выполненного задания и награда твоя</b>"
		else:
			response["text"] = "<b>Send a screenshot of the completed task and the reward is yours</b>"
		return response
	
	def process_get_screen(self, message):
		response = {}
		file_info = bot.get_file(message.photo[0].file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		im = ImageFile(BytesIO(downloaded_file), name = self.user_info.chat_id + '.jpg')
		img = UserImage.objects.create(userI = self.user_info, screenshot = im)
		self.user_info.current_command = ""
		self.user_info.save()
		response["text"] = "Походу, обязательно нужен текст сообщения..."
		response["menu"] = get_menu("reward_menu", self.lang_code)
		return response

	def give_task(self,message):
		response = {}
		if self.user_task == None:
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
				comment = t["comment"],
				userI = self.user_info)

			if user_t.status == "No tasks":
				response["text"] = get_message("no_task_message", self.lang_code)
			else:
				response["text"] = get_message("task_message", self.lang_code, t)

			response["menu"] = get_menu("task_menu", self.lang_code)
		else:
			response["menu"] = get_menu("task_menu", self.lang_code)
			response["text"] = get_message("hula_hoop_message",self.lang_code)
		return response

	def pay(self,message):
		response = {}
		self.user_task.status = "Done"
		self.user_task.save()
		r = {"balance" : self.user_info.pocket,
		"reward" : self.user_task.reward,
		"new_balance" : self.user_info.pocket + self.user_task.reward
		}
		self.user_info.pocket += self.user_task.reward
		self.user_info.save()
		response["text"] = get_message("reward_message", self.lang_code, r)
		response["menu"] = get_menu("main_menu", self.lang_code)
		return response


@bot.message_handler(commands=['start'])
def greetings(message):
	user_ID = Userinfo.objects.filter(chat_id = str(message.chat.id))
	if len(user_ID) == 0:
		keyboard = types.ReplyKeyboardMarkup(row_width = 2, one_time_keyboard = True)
		btn1 = types.KeyboardButton('Русский')
		btn2 = types.KeyboardButton('English')
		keyboard.add(btn1, btn2)
		bot.send_message(message.chat.id, "Здарова", reply_markup = keyboard)
		user = User.objects.create_user(username = "p" + str(message.chat.id), password = None)
		user_info = Userinfo.objects.create(user = user,
			chat_id = message.from_user.id,
			current_command = "Wait for language",
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


@bot.message_handler(content_types=["text","photo"])
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

