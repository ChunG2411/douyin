from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import os

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
from social_network.function import get_absolute_media_path


# Create your views here.
class MusicView(APIView):
    def get(self, request):
        page = request.GET.get('page')
        if not page:
            page = "0"
            
        musics = Music.objects.all()[(int(page)*5):(int(page)+1)*5]
        serializer = MusicSerializer(musics, many=True)
        return Response(response_success(serializer.data), status=200)

    def post(self, request):
        if request.user.id != None:
            request_copy = request.POST.copy()
            request_copy['music'] = request.FILES.copy()['music']
            request_copy['user'] = request.user.id

            serializer = MusicSerializer(data=request_copy)
            if serializer.is_valid():
                serializer.save()
                return Response(response_success(serializer.data), status=201)
            return Response(response_error(serializer.errors), status=400)

        return Response(response_error("Check user login."), status=400)


class MusicDetailView(APIView):
    def get(self, request, pk):
        try:
            music = Music.objects.get(id=pk)
            serializer = MusicSerializer(music)
            return Response(response_success(serializer.data), status=200)
        except Exception as e:
            return Response(response_error(str(e)), status=400)

    def delete(self, request, pk):
        if request.user.id == None:
            return Response(response_error("Check user login."), status=400)

        try:
            music = Music.objects.get(id=pk)
            music = Music.objects.get(id=music.id)
            os.remove(get_absolute_media_path(music.music.url[1:]))
            music.delete()
            return Response(response_success("Delete successful."), status=204)
        except Exception as e:
            return Response(response_error(str(e)), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_music(request):
    page = request.GET.get('page')
    if not page:
        page = "0"

    music = Music.objects.filter(user=request.user)[(int(page)*5):(int(page)+1)*5]
    serializer = MusicSerializer(music, many=True)
    return Response(response_success(serializer.data), status=200)


@api_view(['GET'])
def get_videolist_of_music(request, pk):
    try:
        page = request.GET.get('page')
        if not page:
            page = "0"

        music = Music.objects.get(id=pk)
        videos = Video.objects.filter(music=music)[(int(page)*10):(int(page)+1)*10]   
        serializers = VideoSerializer(videos, many=True)
        return Response(response_success(serializers.data), status=200)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(['GET'])
def get_video(request, pk):
    try:
        video = Video.objects.get(id=pk)
        serializer = VideoSerializer(video, context={'request': request})
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
        comment = CommentVideo.objects.get(id=pk)
        try:
            like = LikeComment.objects.get(user=user, comment=comment)
            like.delete()
            return Response(response_success("Disliked."), status=200)
        except:
            LikeComment.objects.create(user=user, comment=comment)
            return Response(response_success("Liked."), status=200)

    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(['GET'])
def CommentView(request, pk):
    try:
        page = request.GET.get('page')
        if not page:
            page = "0"

        video = Video.objects.get(id=pk)
        try:
            query_parent = request.query_params['parent']
            parent = CommentVideo.objects.get(id=query_parent)
        except:
            parent = None

        all_comments = CommentVideo.objects.filter(video=video, parent=parent)
        cur_page_comment = all_comments[(int(page)*10):(int(page)+1)*10]
        next_page_comment = all_comments[((int(page)+1)*10):(int(page)+2)*10]

        have_more = False
        if len(next_page_comment)>0:
            have_more = True

        serializers = CommentVideoSerializer(cur_page_comment, many=True, context={'request': request, 'have_more': str(have_more)})
        return Response(response_success(serializers.data), status=200)

    except Exception as e:
        return Response(response_error(str(e)), status=400)
