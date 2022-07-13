def f1(extra_info):
	item = [["Дай задание"],["Мой баланс"]]
	return item

def f2(extra_info):
	item = [["Дай другое задание", "Задание выполнено"]]
	return item

def get_menu(title, extra_info = False):
	menus_list = [
		{"title" : "main_menu",
		"function" : f1},
		{"title" : "task_menu",
		"function" : f2}
	]

	for m in menus_list:
		if m["title"] == title:
			return m["function"](extra_info)