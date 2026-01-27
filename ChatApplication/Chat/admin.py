from django.contrib import admin
from .models import User, Conversation, ConversationMember, Message

admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(ConversationMember)
admin.site.register(Message)