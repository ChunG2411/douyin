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


class SingleChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="single_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="single_receiver")
    context = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to='single_chat/%(sender__username)s_%(receiver__username)s')
    status = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_single_chat'
        verbose_name = 'Single Chat'


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField(max_length=255)
    member = models.ManyToManyField(User, blank=True, related_name="group")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_group'
        verbose_name = 'Group'


class GroupChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_sender")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_receiver")
    context = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to="group_chat/%(group__id)s")
    reader = models.ManyToManyField(User, blank=True, related_name="group_reader")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_group_chat'
        verbose_name = 'Group Chat'

    