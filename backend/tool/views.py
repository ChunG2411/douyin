from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import mixins, generics

from django.db.models import Q
from django.shortcuts import  render

from social_network.config import response_error, response_success

from video.models import Video
from video.serializers import VideoSerializer
from user.models import User
from user.serializers import UserDetailSerializer
from .models import SearchRecent, Noti, Chat, Message
from .serializers import NotiSerializer, ChatSerializer

# Create your views here.
@api_view(['GET'])
def SearchVideo(request):
    text = request.query_params['text']

    if request.user:
        searchs = SearchRecent.objects.filter(user=request.user)
        if searchs.count() >= 5:
            searchs.last().delete()
        SearchRecent.objects.create(user=request.user, text=text)         

    videos = Video.objects.filter(descrip__contains=text)
    serializers = VideoSerializer(videos, many=True)

    return Response(response_success(serializers.data), status=200)


@api_view(['GET'])
def SearchUser(request):
    text = request.query_params['text']

    if request.user:
        searchs = SearchRecent.objects.filter(user=request.user)
        if searchs.count() >= 5:
            searchs.last().delete()
        SearchRecent.objects.create(user=request.user, text=text)   

    users = User.objects.filter(Q(first_name__contains=text)|Q(last_name__contains=text)|Q(username__contains=text))
    serializers = UserDetailSerializer(users, many=True)

    return Response(response_success(serializers.data), status=200)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def NotiView(request):
    user = request.user
    noti = Noti.objects.filter(user=user)
    serializer = NotiSerializer(noti, many=True)
    ser_copy = serializer.data
    
    noti_not_read = noti.filter(status=False)
    for i in noti_not_read:
        i.status = True
        i.save()
    
    return Response(response_success(ser_copy), status=200)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def DeleteNotiView(request, pk):
    try:
        noti = Noti.objects.get(id=pk, user=request.user)
        noti.delete()
        return Response(response_success("Delete notification successful."), status=200)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


@permission_classes([permissions.IsAuthenticated])
class ChatView(mixins.ListModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.RetrieveModelMixin,
               generics.GenericAPIView):
    
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        print(id)
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)


def testview(request):
    return render(request, "index.html")