from rest_framework import serializers

from .models import Video, Music, LikeVideo, LikeComment, CommentVideo, Save

class VideoSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    save_count = serializers.SerializerMethodField()

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


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

    def create(self, validated_data):
        music = Music(**validated_data)
        music.save()
        return music

class LikeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeVideo
        fields = '__all__'


class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = '__all__'


class CommentVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVideo
        fields = '__all__'
    
    def create(self, validated_data):
        return super().create(validated_data)


class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = '__all__'