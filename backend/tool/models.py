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

