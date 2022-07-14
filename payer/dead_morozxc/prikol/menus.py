def f1(extra_info,lang_code):
	item = {"ru" : [["Дай задание"],["Мой баланс"]],
			"en" : [["Give me task"],["My balance"]]}
	return item[lang_code]

def f2(extra_info,lang_code):
	item = {"ru" : [["Дай другое задание", "Задание выполнено"]],
			"en" : [["Give me another task", "Job is done"]]}
	return item[lang_code]

def f3(extra_info, lang_code):
	item = {
		"en" : [["English", "Русский"]]
	}
	
	return item[lang_code]

def f4(extra_info, lang_code):
	item = {
		"ru" : [["Получить награду"]],
		"en" : [["Get reward"]]
	}
	return item[lang_code]

def get_menu(title,lang_code, extra_info = False):
	menus_list = [
		{"title" : "main_menu",
		"function" : f1},
		{"title" : "task_menu",
		"function" : f2},
		{"title" : "language_menu",
		"function" : f3},
		{"title" : "reward_menu",
		"function" : f4},
	]

	for m in menus_list:
		if m["title"] == title:
			return m["function"](extra_info,lang_code)