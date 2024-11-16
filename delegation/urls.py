from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='chats'),
    path('chat/', views.view_chats, name='view_chat'),
    #path('chat/message/', views.send_message, name='send_message')
]