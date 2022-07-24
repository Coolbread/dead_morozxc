def f1(extra_info,lang_code):
	item = {"ru": "<b>Твоё задание: </b>" + extra_info.action + "\n" +\
	"<b>Ссылка: </b>" + extra_info.link + "\n" +\
	"<b>Награда: </b>" + str(extra_info.reward) + "\n" +\
	"<b>Дополнительно: </b>" + extra_info.comment,
	"en" : "<b>Your task is: </b>" + extra_info.action + "\n" +\
	"<b>Link: </b>" + extra_info.link + "\n" +\
	"<b>Reward: </b>" + str(extra_info.reward) + "\n" +\
	"<b>Additionaly: </b>" + extra_info.comment}
	return item[lang_code]

def f2(extra_info, lang_code):
	item = {"ru" : "Новых заданий нет!",
			"en" : "I don't have new tasks for you!"}
	return item[lang_code]

def f3(extra_info, lang_code):
	item = {"ru" : "Теперь твой баланс: " + str(extra_info["balance"]) + " + " + str(extra_info["reward"]) + " = " + str(extra_info["new_balance"]),
			"en" : "Now your balance is: " + str(extra_info["balance"]) + " + " + str(extra_info["reward"]) + " = " + str(extra_info["new_balance"])}
	return item[lang_code]

def f4(extra_info,lang_code):
	item = {"ru" : "У тебя уже есть задание!",
			"en" : "You already have a task!"}
	return item[lang_code]

def f5(extra_info,lang_code):
	item = {"en" : "Choose your language"}
	return item[lang_code]

def f6(extra_info,lang_code):
	item = {"ru" : "<b>Получи награду!!!</b>",
			"en" : "<b>Get your reward!!!</b>"}
	return item[lang_code]

def f7(extra_info,lang_code):
	item = {"ru" : "Подожди пока администрация проверит твой скриншот",
			"en" : "Wait until the administration checks your screenshot"}
	return item[lang_code]

def f8(extra_info,lang_code):
	item = {"ru" : "Количество выполненных тобой заданий - " + str(extra_info["count_tasks"]) + "\n" +\
				   "Твой баланс - " + str(extra_info["balance"]),
			"en" : "The number of tasks you have completed - " + str(extra_info["count_tasks"]) + "\n" +\
				   "Your balance - " + str(extra_info["balance"])}
	return item[lang_code]

def f9(extra_info, lang_code):
	item = {"ru" : "Вы успешно отменили задание",
			"en" : "You have successfully skipped the task"}
	return item[lang_code]

def f10(extra_info, lang_code):
	item = {"ru" : "Выбирай способ вывода приколов",
			"en" : "Choose the withdrawal method"}
	return item[lang_code]

def f11(extra_info,lang_code):
	item = {"ru" : "Назад",
			"en" : "Back"}
	return item[lang_code]

def f12(extra_info,lang_code):
	item = {"ru" : "Введите id кошелька. Пример - " + extra_info,
			"en" : "Enter your wallet id. Example - " + extra_info}
	return item[lang_code]

def f13(extra_info,lang_code):
	item = {"ru" : "Хотите воспользоваться прошлым id кошелька - " + extra_info + " ?",
			"en" : "Do you want to use the wallet's past id - " + extra_info + " ?"}
	return item[lang_code]

def f14(extra_info,lang_code):
	item = {"ru" : "Недостаточно средств для вывода! Солнце еще высоко, выполняй задания и возвращайся! Минимальный вывод с " + str(extra_info) + " приколов.",
			"en" : "Not enough funds to withdraw! The sun is still high, complete the tasks and come back! Minimum withdrawal from " + str(extra_info) + " prikols."}
	return item[lang_code]

def f15(extra_info,lang_code):
	item = {"ru" : "Операция прошла успешно! С баланса списано - " + str(extra_info) + " приколов.",
			"en" : "The operation was successful! Debited from the balance - " + str(extra_info) + " prikols."}
	return item[lang_code]

def f16(extra_info,lang_code):
	item = {"ru" : "Неправильно введен id кошелька! Перепроверь!",
			"en" : "The wallet ID was entered incorrectly! Double-check!"}
	return item[lang_code]

def f17(extra_info,lang_code):
	st = ""
	for ex in extra_info:
		st += ex["account"] + "\n"
	item = {"ru" : "Список аккаунтов с помощью которых ты выполнял это задание:" + "\n" + st + "Введите имя аккаунта.",
			"en" : "The list of accounts with which you performed this task:" + "\n" + st + "Enter the account name."}
	return item[lang_code]

def f18(extra_info,lang_code):
	item = {"ru" : "<b>Аккаунт: </b>" + extra_info["ru"],
			"en" : "<b>Account: </b>" + extra_info["en"]}
	return item[lang_code]

def f19(extra_info,lang_code):
	item = {"ru" : "Введите имя аккаунта.",
			"en" : "Enter the account name."}
	return item[lang_code]

def f20(extra_info,lang_code):
	item = {"ru" : "Ты уже пользовался данным юзернеймом!",
			"en" : "You have already used this username!"}
	return item[lang_code]

def f21(extra_info,lang_code):
	item = {"ru" : "Ты успешно привязал аккаунт к заданию! Пора выполнить его!",
			"en" : "You have successfully linked your account to the task! It's time to fulfill it!"}
	return item[lang_code]

def f22(extra_info,lang_code):
	item = {"ru" : "Не привязан аккаунт. Привяжи аккаунт к заданию которое ты выполнил и возвращайся за наградой!",
			"en" : "The account is not linked. Link your account to the task you completed and come back for the reward!"}
	return item[lang_code]

def get_message(title, lang_code, extra_info = False):
	message_list = [
		{"title" : "task_message",
		"function" : f1},
		{"title" : "no_task_message",
		"function" : f2},
		{"title" : "reward_message",
		"function" : f3},
		{"title" : "hula_hoop_message",
		"function" : f4},
		{"title" : "language_message",
		"function" : f5},
		{"title" : "get_reward_message",
		"function" : f6},
		{"title" : "waiting_message",
		"function" : f7},
		{"title" : "profile_message",
		"function" : f8},
		{"title" : "skip_message",
		"function" : f9},
		{"title" : "output_message",
		"function" : f10},
		{"title" : "back_message",
		"function" : f11},
		{"title" : "get_wallet_id_message",
		"function" : f12},
		{"title" : "prev_wallet_id_message",
		"function" : f13},
		{"title" : "small_balance_message",
		"function" : f14},
		{"title" : "pay_message",
		"function" : f15},
		{"title" : "wrong_pattern_id_message",
		"function" : f16},
		{"title" : "get_account_message",
		"function" : f17},
		{"title" : "account_message",
		"function" : f18},
		{"title" : "get_first_time_account_message",
		"function" : f19},
		{"title" : "wrong_username_message",
		"function" : f20},
		{"title" : "success_account_message",
		"function" : f21},
		{"title" : "no_account_message",
		"function" : f22}
	]
	
	for m in message_list:
		if m["title"] == title:
			return m["function"](extra_info, lang_code)