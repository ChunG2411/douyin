from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.core.validators import validate_email

import datetime
from moviepy.editor import *
import os

from social_network.config import response_error, response_success
from .models import User, UserStatus
from .serializers import UserRegisterSerializers, UserDetailSerializer
from video.serializers import LikeVideoSerializer, SaveSerializer, VideoSerializer
from video.models import LikeVideo, Save, Video, Music
from social_network.function import get_absolute_media_path


# Create your views here.

class UserRegisterView(APIView):
    def get(self, request):
        user_list = User.objects.all()
        serializer = UserRegisterSerializers(user_list, many=True)
        return Response(response_success(serializer.data), status=200)

    def post(self, request):
        serializer = UserRegisterSerializers(context = {"request": request}, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(response_success(serializer.data), status=201)
        return Response(response_error(serializer.errors), status=400)


class UserDetailView(APIView):
    def get_user(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except:
            return None
        
    def get(self, request, username):
        user = self.get_user(username)
        if user:
            serializer = UserDetailSerializer(user)
            return Response(response_success(serializer.data), status=200)
        else:
            return Response(response_error("Username don't exist."))
        

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def ModifyUser(request, pk):
    username = request.data.get('username')
    email = request.data.get('email')
    gender = request.data.get('gender')
    birth = request.data.get('birth')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    avatar = request.data.get('avatar')
    address = request.data.get('address')
    introduce = request.data.get('introduce')

    # check username
    user = None
    try:
        user = User.objects.get(id=pk)
    except:
        return Response(response_error("User don't exist."))
    
    if username and username != "":
        try:
            User.objects.get(username=username)
            return Response(response_error("Username already exist."))
        except:
            user.username = username

    # check email
    if email and email != "":
        try:
            User.objects.get(email=email)
            return Response(response_error("Email already exist."), status=400)
        except:
            try:
                validate_email(email)
                user.email = email
            except:
                return Response(response_error("Email invalidated."), status=400)
    
    # check gender
    if gender:
        if gender == "M":
            user.gender = "Male"
        elif gender == "F":
            user.gender = "Female"
        elif gender == "O":
            user.gender = "Other"
        else:
            return Response(response_error("Gender must in [M, F, O]."), status=400)
    
    # check birth
    if birth:
        try:
            birth_split = birth.split('-')
            birth = datetime.date(int(birth_split[0]), int(birth_split[1]), int(birth_split[2]))
            user.birth = birth
        except Exception as e:
            return Response(response_error(str(e)), status=400)
    
    # check name
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.address = address
    user.introduce = introduce

    if avatar:
        user.avatar = avatar
    user.save()
    serializer = UserDetailSerializer(user)

    return Response(response_success(serializer.data), status=200)


class LoginView(APIView):
    def post(self, request):
        username_email = request.data.get('username_email')
        password = request.data.get('password')

        user = None
        try:
            user = User.objects.get(username=username_email)
            username = username_email
        except:
            try:
                user = User.objects.get(email=username_email)
                username = user.username
            except:
                return Response(response_error("Username or Email don't exist."), status=400)

        if not user.check_password(password):
            return Response(response_error("Password inccorect."), status=400)
        
        refresh = TokenObtainPairSerializer.get_token(user)
        token = {
            'access' : str(refresh.access_token),
            'refresh': str(refresh)
        }

        return Response(response_success(token), status=201)


@permission_classes([permissions.IsAuthenticated])
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(response_success("All refresh tokens blacklisted."), status=200)
        refresh_token = self.request.data.get('refresh_token')
        try: 
            token = RefreshToken(token=refresh_token)
            token.blacklist()
        except:
            return Response(response_error("Token is blacklisted."), status=400)
        return Response(response_success("Logout successful."), status=200)

    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_online(request, username):
    user = None
    try:
        user = User.objects.get(username=username)
    except:
        return Response(response_error("User don't exist."), status=400)
    
    status = UserStatus.objects.get_or_create(user=user)
    status[0].status = True
    status[0].save()

    return Response(response_success("User is online."), status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_offline(request, username):
    user = None
    try:
        user = User.objects.get(username=username)
    except:
        return Response(response_error("User don't exist."), status=400)
    
    status = UserStatus.objects.get_or_create(user=user)
    status[0].status = False
    status[0].save()

    return Response(response_success("User is offline."), status=200)


class UserVideoView(APIView):
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except:
            return None
        
    def get(self, request, username):
        user = self.get_user(username)
        if not user:
            return Response(response_error("User don't exist."), status=400)
        
        videos = Video.objects.filter(user=user)
        serializers = VideoSerializer(videos, many=True)

        return Response(response_success(serializers.data), status=200)
    
    def post(self, request, username):
        user = self.get_user(username)
        if not user:
            return Response(response_error("User don't exist."), status=400)
        
        request.data['user'] = user.id
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            if request.data['use_video_music'] == "1":
                # convert mp4 to mp3
                path_video = serializer.data['video'][1:]
                path_music = path_video.replace('video/', 'music/').replace('.mp4', '.mp3')
                video = VideoFileClip(path_video)
                video.audio.write_audiofile(path_music)
                video.close()

                try:
                    music = Music.objects.create(user=user, music=path_music)
                    video = Video.objects.get(id=serializer.data['id']).music = music
                    video.save()
                except:
                    Video.objects.get(id=serializer.data['id']).delete()
                    try:
                        os.remove(get_absolute_media_path(path_video))
                        os.remove(get_absolute_media_path(path_music))
                    except Exception as e:
                        pass
                    return Response(response_error("Error convert to mp3."), status=400)

            return Response(response_success(serializer.data), status=201)
        else:
            return Response(response_error(serializer.errors), status=400)

    
class UserLikeVideoView(APIView):
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except:
            return None
        
    def get(self, request, username):
        user = self.get_user(username)
        if not user:
            return Response(response_error("User don't exist."), status=400)
        
        likes = LikeVideo.objects.filter(user=user)
        serializers = LikeVideoSerializer([i.video for i in likes], many=True)

        return Response(response_success(serializers.data), status=200)
    

class UserSaveView(APIView):
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except:
            return None
        
    def get(self, request, username):
        user = self.get_user(username)
        if not user:
            return Response(response_error("User don't exist."), status=400)
        
        saves = Save.objects.filter(user=user)
        serializers = SaveSerializer([i.video for i in saves], many=True)

        return Response(response_success(serializers.data), status=200)
    
