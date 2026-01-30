from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import User, Chat, ChatMember, Message
from .serializers import (
    UserSerializer,
    ChatSerializer,
    ChatMemberSerializer,
    MessageSerializer,
)


# -----------------------------
# User Views
# -----------------------------
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # adjust as needed


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
# Chat List Views
# -----------------------------
class ChatListViewByUser(generics.ListAPIView):
    # queryset = Chat.objects.all()
    # serializer_class = ChatSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        # chat = get_object_or_404(User,username=username)
        print(request)
        # print(username)
        # user_id = User.objects.filter(username=username).values_list('id')
        # chat = Message.objects.filter(
        #     message_by=user_id
        # ).values_list("chat_name")


        # # print(chat)
        # serializer = ChatSerializer(chat, many=True)

        # return Response(
        #     {
        #         "chat list":serializer.data
        #         }
        #     )
        chat_name_id = ChatMember.objects.filter(
            chat_member_username=user_id
        ).values_list("chat_name_id")
        print(chat_name_id)

        chat = Chat.objects.filter(
            id = chat_name_id[0][0]
        ).values("chat_name")


        print(chat)
        return Response(chat[0])
        # serializer = ChatSerializer(chat, many=True)

        # return Response(serializer.data)

# -----------------------------
# Chat Views
# -----------------------------
class ChatViewByUser(generics.ListAPIView):
    # queryset = Chat.objects.all()
    # serializer_class = ChatSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id, chat_id):
        # chat = get_object_or_404(User,username=username)

        messages = Message.objects.filter(
            message_by=user_id,
            chat_name = chat_id
        ).values("message","message_by","created_at")
        print(messages)
        serializer = MessageSerializer(messages[0])
        # return Response(messages[0])
        return Response(serializer.data)




class ChatDetailView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
# Chat Members Views
# -----------------------------
class ChatMemberListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        members = chat.members.all()
        serializer = ChatMemberSerializer(members, many=True)
        return Response(serializer.data)

    # def post(self, request, chat_id):
    #     chat = get_object_or_404(Chat, id=chat_id)
    #     user_id = request.data.get("user_id")
    #     user = get_object_or_404(User, id=user_id)
    #     member, created = ChatMember.objects.get_or_create(
    #         chat=chat, user=user
    #     )
    #     serializer = ChatMemberSerializer(member)
    #     return Response(serializer.data)


# -----------------------------
# Message Views
# -----------------------------
class MessageListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        messages = chat.messages.order_by("-created_at")[:50]  # last 50 messages
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    # def post(self, request, chat_id):
    #     chat = get_object_or_404(Chat, id=chat_id)
    #     sender = request.user
    #     content = request.data.get("content")

    #     message = Message.objects.create(
    #         chat=chat, sender=sender, content=content
    #     )
    #     serializer = MessageSerializer(message)
    #     return Response(serializer.data)