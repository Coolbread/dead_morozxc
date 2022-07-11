def f1(extra_info):
	item = [["Начать задание", "Задание выполнено"],["Мой баланс"]]
	return item



def get_menu(title, extra_info = False):
	menus_list = [
		{"title" : "main_menu",
		"function" : f1},
	]

	for m in menus_list:
		if m["title"] == title:
			return m["function"](extra_info)