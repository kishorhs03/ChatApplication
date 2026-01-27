from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import User, Conversation, ConversationMember, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    ConversationMemberSerializer,
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
# Conversation Views
# -----------------------------
class ConversationListView(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConversationDetailView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
# Conversation Members Views
# -----------------------------
class ConversationMemberListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        members = conversation.members.all()
        serializer = ConversationMemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)
        member, created = ConversationMember.objects.get_or_create(
            conversation=conversation, user=user
        )
        serializer = ConversationMemberSerializer(member)
        return Response(serializer.data)


# -----------------------------
# Message Views
# -----------------------------
class MessageListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        messages = conversation.messages.order_by("-created_at")[:50]  # last 50 messages
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        sender = request.user
        content = request.data.get("content")

        message = Message.objects.create(
            conversation=conversation, sender=sender, content=content
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data)