from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('user/', views.ChatListViewByUser ),
    # path("<str:username>/", views.ChatListViewByUser.as_view(), name="chatlist-by-user"),
    # path("<str:username>/<str:chat_name>", views.ChatViewByUser.as_view(), name="chat-by-user"),
    path("<int:user_id>/", views.ChatListViewByUser.as_view(), name="chatlist-by-user"),
    path("<int:user_id>/<int:chat_id>/", views.ChatViewByUser.as_view(), name="chat-by-user"),


]
