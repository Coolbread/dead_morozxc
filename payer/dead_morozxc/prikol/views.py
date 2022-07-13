from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from telebot import types 
from .telegram_commands import bot

from django.views.decorators.csrf import csrf_exempt

import traceback

# Create your views here.
@csrf_exempt
def webhook(request):
	try:
		json_string = request.body.decode("utf-8")
		update = types.Update.de_json(json_string)
		bot.process_new_updates([update])
		
		return HttpResponse(status = 200)
	except Exception as e:
		traceback.print_exc()
		print(str(e))

		return HttpResponse(status = 200)

# Create your views here.
@csrf_exempt
def test(request):
	return HttpResponse("Ok? Ok!")