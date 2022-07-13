def f1(extra_info):
	item = "<b>Твоё задание: </b>" + extra_info["action"] + "\n" +\
	"<b>Ссылка: </b>" + extra_info["link"] + "\n" +\
	"<b>Награда: </b>" + str(extra_info["reward"]) + "\n" +\
	"<b>Дополнительно: </b>" + extra_info["comment"]
	return item

def f2(extra_info):
	item = "Новых заданий нет"
	return item


def get_message(title, extra_info = False):
	message_list = [
		{"title" : "task_message",
		"function" : f1},
		{"title" : "no_task_message",
		"function" : f2},
	]
	
	for m in message_list:
		if m["title"] == title:
			return m["function"](extra_info)