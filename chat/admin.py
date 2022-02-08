from django.contrib import admin
from .models import ChatModel
from .models import ReplyModel


admin.site.register(ChatModel)
admin.site.register(ReplyModel)
