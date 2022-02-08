from django.db import models
from user.models import UserModel


class ChatModel(models.Model):
    class Meta:
        db_table = 'chat'

    chat_id = models.CharField(max_length=256)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReplyModel(models.Model):
    class Meta:
        db_table = 'reply'

    # chat = models.ForeignKey(ChatModel,on_delete=models.CASCADE)
    comment_id = models.ForeignKey(ChatModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    recomment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
