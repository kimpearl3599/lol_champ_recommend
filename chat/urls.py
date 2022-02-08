from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('chat/', views.chat_list, name="chat_list"),
    path('chat/<int:id>', views.show_chat, name="show_chat"),

]