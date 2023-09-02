from django.contrib import admin
from .models import Video, Music, LikeVideo, CommentVideo, LikeComment, Save

# Register your models here.
admin.site.register(Video)
admin.site.register(Music)
admin.site.register(LikeVideo)
admin.site.register(CommentVideo)
admin.site.register(LikeComment)
admin.site.register(Save)