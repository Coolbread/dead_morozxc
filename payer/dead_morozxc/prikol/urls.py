from django.conf import settings
from django.conf.urls import url
from . import views

app_name = 'prikol'

urlpatterns = [
	url(r'^bot/process-new-updates/$', views.webhook),
	url(r'^test/$', views.test),
]