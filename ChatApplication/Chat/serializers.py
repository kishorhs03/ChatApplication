from rest_framework import serializers
from .models import User, Chat, ChatMember, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "created_at"]

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "chat_name", "is_group", "created_at"]

class ChatMemberSerializer(serializers.ModelSerializer):
    chat_member_username = UserSerializer(read_only=True)
    chat_name = ChatSerializer(read_only=True)

    class Meta:
        model = ChatMember
        fields = ["id", "chat_name", "chat_member_username"]

class MessageSerializer(serializers.ModelSerializer):
    message_by = UserSerializer(read_only=True)
    chat_name = ChatSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "chat_name", "message_by", "message", "created_at"]