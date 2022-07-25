import telebot
from telebot import types
from django.conf import settings
from django.core.files.images import ImageFile
from django.contrib.auth.models import User

from .models import Userinfo
from .models import UserImage
from .models import UserTask
from .models import WithdrawalMethods
from .models import Withdrawal
from .models import TaskCategory
from .models import	Accounts

from PIL import Image
from io import BytesIO
import psycopg2
import time
import re

from .menus import get_menu
from .messages import get_message

bot = telebot.TeleBot(settings.DEAD_MOROZXC_TOKEN, threaded = False)
bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://langlibclub.com/dead_morozxc/bot/process-new-updates/")

task = {"1" :	{"status" : "Given",
			"task_id" : "1",
			"link" : "https://suda/nado/pereyti",
			"social_network" : "ChinChopa",
			"action" : "Поцелуй свою маму",
			"reward" : 777.777,
			"comment" : "Не надо ниче писать!!!"},
	"2" :	{"status" : "Given",
			"task_id" : "2",
			"link" : "https://hell/lucifer/666",
			"social_network" : "ChinChopa",
			"action" : "Призыв дьявола",
			"reward" : 666.666,
			"comment" : "Надо Жить браза!!!"},
	"3" :	{"status" : "Given",
			"task_id" : "1",
			"link" : "https://suda/nado/pereyti",
			"social_network" : "ChinChopa",
			"action" : "Поцелуй свою маму",
			"reward" : 777.777,
			"comment" : "Не надо ниче писать!!!"}}

class TelegramCommand():
	def get_command(self,command, lang_code):
		commands_list = [
		#{"text" : "Получить новое задание", "function" : },
		{"ru" : "Wait for language", "en" : "Wait for language", "function" : self.process_language},
		{"ru" : "Личный кабинет", "en" : "My profile", "function" : self.my_profile},
		{"ru" : "Задания", "en" : "Tasks", "function" : self.tasks_f, "back_function" : "/main_menu"},
		{"ru" : "Дай другое задание", "en" : "Give me another task", "function" : self.change_task},
		{"ru" : "Отменить задание", "en" : "Skip task", "function" : self.skip_task},
		{"ru" : "process_get_screen", "en" : "process_get_screen", "function" : self.process_get_screen},
		{"ru" : "Получить награду", "en" : "Get reward", "function" : self.pay},
		{"ru" : "Задание выполнено", "en" : "Job is done" , "function" : self.get_screen, "back_function" : "Tasks"},
		{"ru" : "/start", "en" : "/start", "function" : self.greetings},
		{"ru" : "/main_menu","en" : "/main_menu", "function" : self.greetings},
		{"ru" : "Вывод средств", "en" : "Withdrawal of funds", "function" : self.give_output_menu, "back_function" : "/main_menu"},
		{"ru" : "process_output", "en" : "process_output", "function" : self.process_output, "back_function" : "Withdrawal of funds"},
		{"ru" : "process_input_wallet_id", "en" : "process_input_wallet_id", "function" : self.process_input_wallet_id, "back_function" : "Withdrawal of funds"},
		{"ru" : "process_get_category", "en" : "process_get_category", "function" : self.process_get_category, "back_function" : "Tasks"},
		{"ru" : "Привязать аккаунт", "en" : "Link an account", "function" : self.get_account, "back_function" : "Tasks"},
		{"ru" : "process_get_account","en" : "process_get_account", "function" : self.process_get_account}
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
		self.user_task = self.user_info.current_task
		
		self.message = message
		self.lang_code = self.user_info.lang_code
		self.content = message.text
		if self.user_info.current_command:
			self.command = self.get_command(self.user_info.current_command, self.lang_code)
		else:
			self.command = self.get_command(self.content, self.lang_code)

	def execute(self):
		if (self.content == get_message("back_message", self.lang_code)): 
			self.command = self.get_command(self.user_info.prev_func, "en")
			self.command = self.get_command(self.command["back_function"], "en")

		r = self.command["function"](self.message)
		return r
	
	def process_language(self, message):
		# Check if language set correctly 
		response = {}
		if (self.content == "Русский"):
			self.lang_code = "ru"
			self.user_info.current_command = None
			self.user_info.lang_code = "ru"
			self.user_info.save()
			response["text"] = "<b>Пора выполнять задания!</b>"
			response["menu"] = get_menu("main_menu", self.lang_code)
		elif (self.content == "English"):
			self.lang_code = "en"
			self.user_info.current_command = None
			self.user_info.lang_code = "en"
			self.user_info.save()
			response["text"] = "<b>It's time to complete the tasks!</b>"
			response["menu"] = get_menu("main_menu", self.lang_code)
		else:
			response["text"] = get_message("wrong_language", "en")
			response["menu"] = get_menu("language_menu", "en")
			return response
	
	def greetings(self, message):
		response = {}
		response["menu"] = get_menu("main_menu", self.lang_code)
		self.user_info.prev_func = ""
		self.user_info.current_command = ""
		self.user_info.save()
		if self.lang_code == "ru":
			response["text"] = "<b>Здарова!</b>"
		else:
			response["text"] = "<b>Hello!</b>"
		return response

	def my_profile(self,message):
		response = {}
		info = {
			"count_tasks" : self.user_info.count_tasks,
			"balance" : self.user_info.pocket
		}
		response["text"] = get_message("profile_message", self.lang_code, info)
		return response

	def tasks_f(self,message):
		response = {}
		self.user_info.prev_func = "Tasks"
		self.user_info.current_command = ""
		
		if self.user_task:
			if self.user_task.category.need_account:
				extra = {"ru" : self.user_task.account.account_name,
						"en" : self.user_task.account.account_name}
				response["text"] = get_message("task_message",self.lang_code, self.user_task) + "\n" +\
				get_message("account_message", self.lang_code, extra)
				response["menu"] = get_menu("if_have_task_menu", self.lang_code)					
			else:
				response["text"] = get_message("task_message",self.lang_code, self.user_task)
				response["menu"] = get_menu("if_have_task_menu", self.lang_code)
		else:
			category_list = TaskCategory.objects.values("ru_name","en_name")
			self.user_info.current_command = "process_get_category"
			if self.lang_code == "ru":
				response["text"] = "<b>Выбери категорию задания.</b>"
			else:
				response["text"] = "<b>Choose a task category.</b>"
			response["menu"] = get_menu("task_category_menu", self.lang_code, category_list)
		
		self.user_info.save()
		return response

	def process_get_category(self,message):
		response = {}
		try:
			if self.lang_code == "ru":
				category = TaskCategory.objects.get(ru_name = self.content)
			else:
				category = TaskCategory.objects.get(en_name = self.content)
		except:
			category = None
		if category:
			if category.need_account:
				self.user_info.current_command = "process_get_account"
				self.user_info.name_category = category.en_name
				accounts = Accounts.objects.filter(userI = self.user_info, category = category)
				if len(accounts) != 0:
					account_list = []
					for a in accounts:
						acc = {"account" : a.account_name}
						account_list.append(acc)
					response["text"] = get_message("get_account_message", self.lang_code,account_list)
					response["menu"] = get_menu("back_menu",self.lang_code)
				else:
					response["text"] = get_message("get_first_time_account_message",self.lang_code)
					response["menu"] = get_menu("back_menu", self.lang_code)
			else:
				self.user_info.current_command = ""
				t = task[category.category_id]
				if t["status"] != "No tasks":			
					user_t = UserTask.objects.create(status = t["status"],
						task_id = t["task_id"],
						link = t["link"],
						social_network = t["social_network"],
						action = t["action"],
						reward = t["reward"],
						comment = t["comment"],
						userI = self.user_info,
						category = category)
					response["text"] = get_message("task_message", self.lang_code, user_t)
					response["menu"] = get_menu("main_menu", self.lang_code)

				else:
					response["text"] = get_message("no_task_message", self.lang_code)
					response["menu"] = get_menu("main_menu", self.lang_code)
		else:
			category_list = TaskCategory.objects.values("ru_name","en_name")
			self.user_info.current_command = "process_get_category"
			response["text"] = get_message("wrong_category_message", self.lang_code)
			response["menu"] = get_menu("task_category_menu", self.lang_code, category_list)
		self.user_info.save()
		return response

	def get_account(self,message):
		self.user_info.current_command = "process_get_account"
		self.user_info.prev_func = "Link an account"
		response = {}
		task_list = UserTask.objects.filter(userI = self.user_info,task_id = self.user_task.task_id, status = "Done")
		if len(task_list) != 0:
			account_list = []
			for ta in task_list:
				if ta.account.account_name:
					acc = {"account" : ta.account.account_name}
					account_list.append(acc)
			if len(account_list) == 0:
				account_list = None
		else:
			account_list = None
		if account_list:
			response["text"] = get_message("get_account_message", self.lang_code, account_list)
		else:
			response["text"] = get_message("get_first_time_account_message", self.lang_code)
		response["menu"] = get_menu("back_menu", self.lang_code)
		self.user_info.save()
		return response

	def process_get_account(self,message):
		response = {}
		self.user_info.current_command = ""
		self.user_info.prev_func = "Tasks"

		category = TaskCategory.objects.get(en_name = self.user_info.name_category)
		try:
			account = Accounts.objects.get(account_name = self.content)
		except:
			account = None
		fl = True
		if account:
			t = task[category.category_id]
			if t["status"] != "No tasks":			
				user_t = UserTask.objects.create(status = t["status"],
					task_id = t["task_id"],
					link = t["link"],
					social_network = t["social_network"],
					action = t["action"],
					reward = t["reward"],
					comment = t["comment"],
					userI = self.user_info,
					category = category,
					account = account)
				response["text"] = get_message("task_message", self.lang_code, user_t)
				response["menu"] = get_menu("if_have_task_menu", self.lang_code)

			else:
				response["text"] = get_message("no_task_message", self.lang_code)
				response["menu"] = get_menu("main_menu", self.lang_code)
		else:
			account = Accounts.objects.create(userI = self.user_info,
			category = category,
			account_name = self.content)
			t = task[category.category_id]
			if t["status"] != "No tasks":			
				user_t = UserTask.objects.create(status = t["status"],
					task_id = t["task_id"],
					link = t["link"],
					social_network = t["social_network"],
					action = t["action"],
					reward = t["reward"],
					comment = t["comment"],
					userI = self.user_info,
					category = category,
					account = account)
				response["text"] = get_message("task_message", self.lang_code, user_t)
				response["menu"] = get_menu("if_have_task_menu", self.lang_code)

			else:
				response["text"] = get_message("no_task_message", self.lang_code)
				response["menu"] = get_menu("main_menu", self.lang_code)
		self.user_info.current_task = user_t
		self.user_info.save()
		return response



	def get_screen(self,message):
		response = {}
		self.user_info.prev_func = "Job is done"
		self.user_info.current_command = "process_get_screen"
		self.user_info.save()

		if self.lang_code == "ru":
			response["text"] = "<b>Кидай скриншот выполненного задания и награда твоя</b>"
		else:
			response["text"] = "<b>Send a screenshot of the completed task and the reward is yours</b>"
		response["menu"] = get_menu("back_menu", self.lang_code)
		return response
	
	def process_get_screen(self, message):
		response = {}
		file_info = bot.get_file(message.photo[0].file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		im = ImageFile(BytesIO(downloaded_file), name = self.user_info.chat_id + '.jpg')
		img = UserImage.objects.create(userI = self.user_info, screenshot = im)
		self.user_info.current_command = ""
		self.user_info.save()
		self.user_task.userImage = img
		self.user_task.save()
		response["text"] = get_message("get_reward_message", self.lang_code)
		response["menu"] = get_menu("reward_menu", self.lang_code)
		return response

	"""def give_task(self,message):
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
		if t["status"] != "No tasks":			
			user_t = UserTask.objects.create(status = t["status"],
				task_id = t["task_id"],
				link = t["link"],
				social_network = t["social_network"],
				action = t["action"],
				reward = t["reward"],
				comment = t["comment"],
				userI = self.user_info)
			response["text"] = get_message("task_message", self.lang_code, t)
			response["menu"] = get_menu("main_menu", self.lang_code)

		else:
			response["text"] = get_message("no_task_message", self.lang_code)
			response["menu"] = get_menu("main_menu", self.lang_code)
		return response"""

	def skip_task(self,message):
		response = {}
		response["text"] = get_message("skip_message", self.lang_code)
		self.user_task.status = "Skipped"
		self.user_task.save()
		self.user_info.current_task = None
		self.user_info.save()
		response["menu"] = get_menu("main_menu", self.lang_code)
		return response

	def change_task(self,message):
		response = {}
		self.user_task.status = "Skipped"
		self.user_task.save()
		self.user_info.current_command = "process_get_category"
		self.user_info.save()

		category_list = TaskCategory.objects.values("ru_name","en_name")

		if self.lang_code == "ru":
			response["text"] = "<b>Выбери категорию задания.</b>"
		else:
			response["text"] = "<b>Choose a task category.</b>"
		response["menu"] = get_menu("task_category_menu", self.lang_code, category_list)

		return response		

	def pay(self,message):
		response = {}
		if self.user_info.force_check == False:
			self.user_task.status = "Done"
			self.user_task.save()
			r = {"balance" : self.user_info.pocket,
			"reward" : self.user_task.reward,
			"new_balance" : self.user_info.pocket + self.user_task.reward
			}
			self.user_info.pocket += self.user_task.reward
			self.user_info.count_tasks += 1
			self.user_info.save()
			response["text"] = get_message("reward_message", self.lang_code, r)
		else:
			response["text"] = get_message("waiting_message", self.lang_code)
		response["menu"] = get_menu("main_menu", self.lang_code)
		return response

	def give_output_menu(self,message):
		output_list = WithdrawalMethods.objects.values("name").filter(is_active = True)
		self.user_info.current_command = "process_output"
		self.user_info.prev_func = "Withdrawal of funds"
		self.user_info.save()
		response = {}
		response["menu"] = get_menu("output_menu", self.lang_code, output_list)
		response["text"] = get_message("output_message", self.lang_code)
		return response

	def process_output(self,message):
		self.user_info.withdrawal_method = self.content
		method = WithdrawalMethods.objects.get(name = self.content)
		response = {}
		if self.user_info.pocket > method.min_withdrawal:
			self.user_info.prev_func = "process_output"
			self.user_info.current_command = "process_input_wallet_id"
			self.user_info.save()
			if self.user_info.pocket_id == None:
				response["text"] = get_message("get_wallet_id_message", self.lang_code, method.example)
				response["menu"] = get_menu("back_menu", self.lang_code)
			else:
				response["text"] = get_message("prev_wallet_id_message", self.lang_code, self.user_info.pocket_id)
				response["menu"] = get_menu("yes_no_menu", self.lang_code)
		else:
			response["text"] = get_message("small_balance_message", self.lang_code, method.min_withdrawal)
			response["menu"] = get_menu("back_menu", self.lang_code)
		return response

	def process_input_wallet_id(self,message):
		response = {}
		try:
			method = WithdrawalMethods.objects.get(name = self.user_info.withdrawal_method)
		except:
			method = None
		if self.content == "Да" or self.content == "Yes":
			response["text"] = get_message("pay_message",self.lang_code, self.user_info.pocket)
			withdrawal = Withdrawal.objects.create(user = self.user_info,
				method = method,
				outcome = self.user_info.pocket,
				payout_id = self.user_info.pocket_id)
			self.user_info.current_command = ""
			self.user_info.pocket = 0
			self.user_info.save()
			response["menu"] = get_menu("main_menu",self.lang_code)
		elif self.content == "Нет" or self.content == "No":
			self.user_info.pocket_id = None
			self.user_info.save()
			response["text"] = get_message("get_wallet_id_message", self.lang_code, method.example)
			response["menu"] = get_menu("back_menu", self.lang_code)
		else:
			regex = re.compile(method.regex)
			if re.fullmatch(regex, self.content):
				response["text"] = get_message("pay_message", self.lang_code, self.user_info.pocket)
				withdrawal = Withdrawal.objects.create(user = self.user_info,
					method = method,
					outcome = self.user_info.pocket,
					payout_id = self.content)
				self.user_info.pocket_id = self.content
				self.user_info.pocket = 0
				self.user_info.current_command = ""
				self.user_info.save()
				response["menu"] = get_menu("main_menu", self.lang_code)
			else:
				response["text"] = get_message("wrong_pattern_id_message", self.lang_code)
				response["menu"] = get_menu("back_menu", self.lang_code)
		return response

@bot.message_handler(commands=['start'])
def greetings(message):
	user_ID = Userinfo.objects.filter(chat_id = str(message.chat.id))
	if len(user_ID) == 0:
		response = {}
		response["menu"] = get_menu("language_menu", "en")
		response["text"] = get_message("language_message", "en")
		keyboard = telebot.types.ReplyKeyboardMarkup()
		for m in response["menu"]:
			keyboard.row(*m)
		bot.send_message(message.chat.id, response["text"], reply_markup = keyboard)
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

