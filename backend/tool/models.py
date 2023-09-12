import os
import uuid
from django.db import models

from user.models import User
from video.models import Video

# Create your models here.
class SearchRecent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_search")
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_search_recent'
        verbose_name = 'Search recent'


class Noti(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_noti")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_noti")
    TYPE_CHOICES = (
        ('1', 'like_video'),
        ('2', 'comment_video'),
        ('3', 'like_comment'),
        ('4', 'comment_comment'),
        ('5', 'follow')
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    context = models.TextField()
    status = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_noti'
        verbose_name = 'Notification'


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_user")
    name = models.TextField(max_length=255, blank=True, null=True)
    member = models.ManyToManyField(User, blank=True, related_name="chat_member")
    TYPE_CHOICES = (
        ('1', 'single'),
        ('2', 'group')
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    avatar = models.ImageField(upload_to="chat/avatar", blank=True, null=True)
    last_action = models.DateTimeField(blank=True, null=True)
    last_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-last_action']
        db_table = 'tb_chat'
        verbose_name = 'Chat'


def message_file_upload_path(instance, filename):
    group_id = instance.receiver.id
    folder_path = f"chat/file/{group_id}"
    return os.path.join(folder_path, filename)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="receiver")
    context = models.TextField(null=True, blank=True)
    media = models.FileField(null=True, blank=True, upload_to=message_file_upload_path)
    reader = models.ManyToManyField(User, blank=True, related_name="reader")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_message'
        verbose_name = 'Message'

