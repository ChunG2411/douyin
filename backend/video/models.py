from django.db import models
from django.core.validators import FileExtensionValidator

from user.models import User

import uuid

# Create your models here.

class Music(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_music")
    name = models.CharField(max_length=255, default='')
    music = models.FileField(upload_to="music", validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_music'
        verbose_name = 'Music'

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = "Music created by "+self.user.get_full_name
        super(Music, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username
    

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_video")
    descrip = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to="video", validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    music = models.ForeignKey(Music, on_delete=models.SET_NULL, related_name="video_music", null=True, blank=True)
    public = models.BooleanField(default=True)
    view = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_video'
        verbose_name = 'Video'
    
    @property
    def like_count(self):
        like = LikeVideo.objects.filter(video=self)
        return like.count()
    
    @property
    def comment_count(self):
        comment = CommentVideo.objects.filter(video=self)
        return comment.count()
    
    @property
    def save_count(self):
        save = Save.objects.filter(video=self)
        return save.count()
    
    def __str__(self):
        return self.user.username


class LikeVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_video_like")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_like")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_video_like'
        verbose_name = 'Video Like'


class CommentVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_video_comment")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_comment")
    context = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="comment_children", null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_video_comment'
        verbose_name = 'Video Comment'


class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment_like")
    comment = models.ForeignKey(CommentVideo, on_delete=models.CASCADE, related_name="comment_like")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_comment_like'
        verbose_name = 'Comment Like'
    


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_save")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_save")
    create_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_save'
        verbose_name = 'Save'


