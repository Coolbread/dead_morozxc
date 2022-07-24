from django.contrib import admin

from .models import WithdrawalMethods
from .models import TaskCategory
# Register your models here.

admin.site.register(WithdrawalMethods)
admin.site.register(TaskCategory)