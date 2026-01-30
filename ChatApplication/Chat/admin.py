from django.contrib import admin
from .models import User, Chat, ChatMember, Message

admin.site.register(User)
admin.site.register(Chat)
admin.site.register(ChatMember)
admin.site.register(Message)