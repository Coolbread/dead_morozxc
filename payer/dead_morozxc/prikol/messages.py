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
	]
	
	for m in message_list:
		if m["title"] == title:
			return m["function"](extra_info, lang_code)