def f1(extra_info,lang_code):
	item = {"ru" : [["Задания"],["Личный кабинет"],["Вывод средств"]],
			"en" : [["Tasks"],["My profile"],["Withdrawal of funds"]]}
	return item[lang_code]

def f2(extra_info,lang_code):
	item = {"ru" : [["Дай задание"],["Назад"]],
			"en" : [["Give me task"],["Back"]]}
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

def f5(extra_info, lang_code):
	item = {
		"ru" : [["Дай другое задание", "Задание выполнено"],["Отменить задание","Назад"]],
		"en" : [["Give me another task","Job is done"], ["Skip task","Back"]]
	}
	return item[lang_code]

def f6(extra_info,lang_code):
	menu = []
	for ex in extra_info:
		menu.append([ex["name"]])
	if lang_code == "ru":
		menu += [["Назад"]]
	else:
		menu += [["Back"]]
	return menu

def f7(extra_info,lang_code):
	item = {"ru" : [["Назад"]],
			"en" : [["Back"]]}
	return item[lang_code]

def f8(extra_info,lang_code):
	item = {"ru" : [["Да","Нет"],["Назад"]],
			"en" : [["Yes","No"],["Back"]]}
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
		{"title" : "if_have_task_menu",
		"function" : f5},
		{"title" : "output_menu",
		"function" : f6},
		{"title" : "back_menu",
		"function" : f7},
		{"title" : "yes_no_menu",
		"function" : f8}
	] 

	for m in menus_list:
		if m["title"] == title:
			return m["function"](extra_info,lang_code)