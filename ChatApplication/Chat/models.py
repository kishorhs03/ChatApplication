from django.db import models
# from django.contrib.auth.models import AbstractUser

# -----------------------------
# Users Table
# -----------------------------
class User(models.Model):
    # AbstractUser already provides: username, password, email, first_name, last_name
    # You can extend with custom fields if needed
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)   # store hashed passwords, not plain text!
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# -----------------------------
# Conversations Table
# -----------------------------
class Chat(models.Model):
    chat_name = models.CharField(max_length=100, blank=True, null=True)  # For group chats
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # message_id = models.CharField(max_length=100, blank=False)
    # message_id = models.ForeignKey(
    #     Message, on_delete=models.CASCADE, related_name="messages"
    # )

    def __str__(self):
        return self.chat_name if self.chat_name else f"Chat {self.id}"

class ChatMember(models.Model):
    chat_name = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="members"
    )
    chat_member_username = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_memberships"
    )


# -----------------------------
# Messages Table
# -----------------------------
class Message(models.Model):
    
    message_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    chat_name = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username}"
    

# -----------------------------
# Conversation Members Table
# -----------------------------
# class ConversationMember(models.Model):
#     conversation = models.ForeignKey(
#         Conversation, on_delete=models.CASCADE, related_name="members"
#     )
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="conversations"
#     )
#     joined_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("conversation", "user")  # Prevent duplicate membership

#     def __str__(self):
#         return f"{self.user.username} in {self.conversation}"


    
'''
    Why This Structure Works
- User: Extends Django’s built-in AbstractUser for authentication and flexibility.
- Conversation: Represents either a group or one-on-one chat.
- ConversationMember: Manages the many-to-many relationship between users and conversations.
- Message: Stores actual chat content, linked to both sender and conversation.

🔑 Notes
- unique_together in ConversationMember ensures a user can’t join the same conversation twice.
- related_name makes reverse queries easy:
- user.conversations.all() → all conversations a user belongs to.
- conversation.messages.all() → all messages in a conversation.
- You can later add indexes (like conversation_id + created_at) for performance.

    '''