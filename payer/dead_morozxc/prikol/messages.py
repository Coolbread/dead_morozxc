def f1(extra_info,lang_code):
	item = {"ru": "<b>Твоё задание: </b>" + extra_info["action"] + "\n" +\
	"<b>Ссылка: </b>" + extra_info["link"] + "\n" +\
	"<b>Награда: </b>" + str(extra_info["reward"]) + "\n" +\
	"<b>Дополнительно: </b>" + extra_info["comment"],
	"en" : "<b>Your task is: </b>" + extra_info["action"] + "\n" +\
	"<b>Link: </b>" + extra_info["link"] + "\n" +\
	"<b>Reward: </b>" + str(extra_info["reward"]) + "\n" +\
	"<b>Additionaly: </b>" + extra_info["comment"]}
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
		"function" : f9}
	]
	
	for m in message_list:
		if m["title"] == title:
			return m["function"](extra_info, lang_code)