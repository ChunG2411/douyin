from rest_framework import serializers

from .models import Video, Music, LikeVideo, LikeComment, CommentVideo, Save
from user.models import User
from user.serializers import UserDetailSerializer


class VideoSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    save_count = serializers.SerializerMethodField()
    user_infor = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def create(self, validated_data):
        video = Video(**validated_data)
        video.save()
        return video

    def get_like_count(self,  obj):
        return obj.like_count

    def get_comment_count(self,  obj):
        return obj.comment_count

    def get_save_count(self,  obj):
        return obj.save_count

    def get_user_infor(self, obj):
        user_serializer = UserDetailSerializer(obj.user)
        return user_serializer.data

    def get_liked(self, obj):
        liked = LikeVideo.objects.filter(video=obj)
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user and user.username in [like.user.username for like in liked]:
            return True
        else:
            return False

    def get_saved(self, obj):
        saved = Save.objects.filter(video=obj)
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user and user.username in [save.user.username for save in saved]:
            return True
        else:
            return False


class MusicSerializer(serializers.ModelSerializer):
    user_infor = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = '__all__'

    def create(self, validated_data):

        music = Music(**validated_data)
        music.save()
        return music
    
    def get_user_infor(self, obj):
        user_serializer = UserDetailSerializer(obj.user)
        return user_serializer.data
    
    def get_video_count(self, obj):
        video = Video.objects.filter(music=obj.id)
        return video.count()


class LikeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeVideo
        fields = '__all__'


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = '__all__'


class CommentVideoSerializer(serializers.ModelSerializer):
    user_infor = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    child_count = serializers.SerializerMethodField()

    class Meta:
        model = CommentVideo
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def get_user_infor(self, obj):
        user_serializer = UserDetailSerializer(obj.user)
        return user_serializer.data

    def get_liked(self, obj):
        liked = LikeComment.objects.filter(comment=obj)
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user and user.username in [like.user.username for like in liked]:
            return True
        else:
            return False

    def get_like_count(self, obj):
        liked = LikeComment.objects.filter(comment=obj)
        return liked.count()

    def get_child_count(self, obj):
        child = CommentVideo.objects.filter(video=obj.video, parent=obj.id)
        return child.count()


class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = '__all__'
