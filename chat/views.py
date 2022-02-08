from django.shortcuts import render, redirect
from .models import ChatModel
from .models import UserModel
from .models import ReplyModel
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/chat')
    else:
        return redirect('/sign-in')


@login_required
def chat_list(request):
    if request.method == 'GET':
        user_list = UserModel.objects.all().exclude(username=request.user.username).exclude(is_superuser=True)
        print(user_list)
        return render(request, 'chat_list.html', {'user_list': user_list})


@login_required
def show_chat(request, id):
    if request.method == 'GET':
        
        user_list = UserModel.objects.all().exclude(username=request.user.username).exclude(is_superuser=True)
        chat_user = get_user_model().objects.get(id=id)
        all_chats = ChatModel.objects.filter(
            Q(chat_id=id, author_id=request.user.id) | Q(chat_id=request.user.id, author_id=id)).order_by(
            'created_at')

        return render(request, 'user_chat.html', {'chat_user': chat_user, 'user_list': user_list, 'all_chats': all_chats})

    elif request.method == 'POST':
        user = request.user
        comment = request.POST.get('comment', '')
        chat_id = id

        if user == request.user:
            my_chat = ChatModel.objects.create(author=user, comment=comment, chat_id=chat_id)
            my_chat.save()
            return redirect('/chat/' + str(id))
