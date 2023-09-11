from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import (VideoSerializer,
                          MusicSerializer,
                          CommentVideoSerializer)
from .models import (Music,
                    Video,
                    Save,
                    LikeVideo,
                    LikeComment,
                    CommentVideo)
from social_network.config import response_error, response_success


# Create your views here.
class MusicView(APIView):
    def get(self, request, pk):
        try:
            music = Music.objects.get(id=pk)
            serializer = MusicSerializer(music)
            return Response(response_success(serializer.data), status=200)
        except Exception as e:
            return Response(response_error(str(e)), status=400)


@api_view(['GET'])
def get_videolist_of_music(request, pk):
    try:
        music = Music.objects.get(id=pk)
        videos = Video.objects.filter(music=music)
        serializers = VideoSerializer(videos, many=True)
        return Response(response_success(serializers.data), status=200)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(['GET'])
def get_video(request, pk):
    try:
        video = Video.objects.get(id=pk)
        serializer = VideoSerializer(video)
        return Response(response_success(serializer.data), status=200)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def SaveVideoView(request, pk):
    user = request.user
    try:
        video = Video.objects.get(id=pk)
        try:
            save = Save.objects.get(user=user, video=video)
            save.delete()
            return Response(response_success("UnSaved."))
        except:
            Save.objects.create(user=user, video=video)
            return Response(response_success("Saved."))

    except Exception as e:
        return Response(response_error(str(e)), status=400)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def LikeVideoView(request, pk):
    user = request.user
    try:
        video = Video.objects.get(id=pk)
        try:
            like = LikeVideo.objects.get(user=user, video=video)
            like.delete()
            return Response(response_success("Disliked."))
        except:
            LikeVideo.objects.create(user=user, video=video)
            return Response(response_success("Liked."))

    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def CommentVideoView(request, pk):
    user_id = request.user.id
    request_copy = request.data.copy()
    request_copy['user'] = user_id
    request_copy['video'] = pk

    serializer = CommentVideoSerializer(data=request_copy)
    if serializer.is_valid():
        serializer.save()
        return Response(response_success(serializer.data), status=201)
    else:
        return Response(response_error(serializer.errors), status=400)
    

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def DeleteCommentView(request, pk):
    user_id = request.user.id
    try:
        comment = CommentVideo.objects.get(id=pk, user=user_id)
        comment.delete()
        return Response(response_success("Delete successful."), status=204)
    except Exception as e:
        return Response(response_error(str(e)), status=400)

    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def LikeCommentView(request, pk):
    user = request.user
    try:
        comment = CommentVideo.objects.get(id=pk, user=user)
        try:
            like = LikeComment.objects.get(user=user, comment=comment)
            like.delete()
            return Response(response_success("Comment disliked."), status=200)
        except:
            LikeComment.objects.create(user=user, comment=comment)
            return Response(response_success("Comment liked."), status=200)
        
    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(['GET'])
def CommentView(request, pk):
    try:
        video = Video.objects.get(id=pk)
        comments = CommentVideo.objects.filter(video=video)
        serializers = CommentVideoSerializer(comments, many=True)
        return Response(response_success(serializers.data), status=200)

    except Exception as e:
        return Response(response_error(str(e)), status=400)
    
