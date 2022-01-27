from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('user/follow/<int:id>', views.user_follow, name='user-follow')
    
]
