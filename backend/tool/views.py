from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.db.models import Q

from social_network.config import response_error, response_success
from video.models import Video
from video.serializers import VideoSerializer
from user.models import User
from user.serializers import UserDetailSerializer
from .models import SearchRecent, Noti, Chat, Message
from .serializers import NotiSerializer, ChatSerializer, MessageSerializer

# Create your views here.


@api_view(['GET'])
def SearchVideo(request):
    text = request.query_params['text']

    page = request.GET.get('page')
    if not page:
        page = "0"

    if request.user.id != None:
        searchs = SearchRecent.objects.filter(user=request.user)
        if searchs.count() >= 5:
            searchs.last().delete()
        SearchRecent.objects.create(user=request.user, text=text)

    videos = Video.objects.filter(descrip__contains=text)[
        (int(page)*5):(int(page)+1)*5]
    serializers = VideoSerializer(
        videos, many=True, context={'request': request})

    return Response(response_success(serializers.data), status=200)


@api_view(['GET'])
def SearchUser(request):
    text = request.query_params['text']

    page = request.GET.get('page')
    if not page:
        page = "0"

    if request.user.id != None:
        searchs = SearchRecent.objects.filter(user=request.user)
        if searchs.count() >= 5:
            searchs.last().delete()
        SearchRecent.objects.create(user=request.user, text=text)

    users = User.objects.exclude(id=request.user.id).filter(Q(first_name__contains=text) | Q(
        last_name__contains=text) | Q(username__contains=text))[(int(page)*10):(int(page)+1)*10]
    serializers = UserDetailSerializer(users, many=True)

    return Response(response_success(serializers.data), status=200)


@api_view(['GET'])
def RecentSearch(request):
    if request.user.id != None:
        search_recent = SearchRecent.objects.filter(user=request.user)[:5]
        return Response(response_success([i.text for i in search_recent]))
    else:
        return Response(response_success(""))


@api_view(['GET'])
def SuggestSearch(request):
    text = request.query_params['text']
    suggest = SearchRecent.objects.filter(text__istartswith=text)[:5]
    return Response(response_success(list(set([i.text for i in suggest]))))


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def SearchChat(request):
    text = request.query_params['text']
    chats = Chat.objects.filter(
        member__id=request.user.id, name__contains=text)
    serializers = ChatSerializer(
        chats, many=True, context={'request': request})
    return Response(response_success(serializers.data), status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def SearchMessage(request, pk):
    text = request.query_params['text']
    try:
        chat = Chat.objects.get(id=pk)
        message = Message.objects.filter(receiver=chat, context__contains=text)
        serializers = MessageSerializer(message, many=True, context={'have_more': False})
        return Response(response_success(serializers.data), status=200)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def NotiView(request):
    page = request.GET.get('page')
    if not page:
        page = "0"

    noti = Noti.objects.filter(user=request.user)[
        (int(page)*5):(int(page)+1)*5]
    serializer = NotiSerializer(noti, many=True)
    ser_copy = serializer.data

    for i in noti:
        if i.status == False:
            i.status = True
            i.save()

    return Response(response_success(ser_copy), status=200)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def DeleteNotiView(request, pk):
    try:
        noti = Noti.objects.get(id=pk, user=request.user)
        noti.delete()
        return Response(response_success("Delete notification successful."), status=204)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


class ChatView(APIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        chats = self.queryset.filter(member__id=request.user.id)
        return Response(response_success(self.serializer_class(chats, many=True,  context={'request': request}).data), status=200)

    def delete(self, request):
        chat_id = request.GET.get('id')
        try:
            self.queryset.get(id=chat_id, user=request.user).delete()
            return Response(response_success("Delete successful."), status=204)
        except Exception as e:
            return Response(response_error(str(e)), status=400)

    def post(self, request):
        member = request.data.get('member')

        if not member or member == "":
            return Response(response_error("Member is required."), status=400)

        request_copy = request.data.copy()
        request_copy['user'] = request.user.id
        request_copy['member'] = member

        serializer = self.serializer_class(data=request_copy)
        if serializer.is_valid():
            serializer.save()
            return Response(response_success(serializer.data), status=201)
        else:
            return Response(response_error(serializer.errors), status=400)

    def put(self, request):
        chat_id = request.GET.get('id')
        name = request.data.get('name')
        avatar = request.data.get('avatar')

        try:
            chat = Chat.objects.get(id=chat_id)
            if name:
                chat.name = name
            if avatar:
                chat.avatar = avatar
            chat.save()
            serializer = ChatSerializer(chat, context={'request': request})
            return Response(response_success(serializer.data), status=201)
        except Exception as e:
            return Response(response_error(str(e)), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_member_of_chat(request, pk):
    try:
        chat = Chat.objects.get(id=pk)
        serializer = UserDetailSerializer(chat.member, many=True)
        return Response(response_success(serializer.data), status=201)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_member_to_chat(request, pk):
    member = request.POST.get('member')
    member_list = member.replace(' ', '').split(',')
    try:
        chat = Chat.objects.get(id=pk)
        if chat.type == "1":
            return Response(response_error("Couldn't add member to this chat."), status=400)
        for i in member_list:
            user = User.objects.get(username=i)
            chat.member.add(user)
        return Response(response_success("Add member succesful."), status=201)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_member_to_chat(request, pk):
    member = request.POST.get('member')
    try:
        chat = Chat.objects.get(id=pk)
        if chat.type == "1":
            return Response(response_error("Couldn't remove member to this chat."), status=400)
        user = User.objects.get(username=member)

        if user.username == chat.user.username:
            chat.delete()
        else:
            chat.member.remove(user)

        return Response(response_success("Remove member succesful."), status=200)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


class MessageView(APIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        page = request.GET.get('page')
        if not page:
            page = "0"
        try:
            chat = Chat.objects.get(id=pk, member__id=request.user.id)
            message = self.queryset.filter(receiver=chat)[
                (int(page)*20):((int(page)+1)*20)]
            message_next = self.queryset.filter(receiver=chat)[
                ((int(page)+1)*20):((int(page)+2)*20)]

            have_more = False
            if len(message_next) > 0:
                have_more = True

            for i in message:
                i.reader.add(request.user)

            serializer = self.serializer_class(message, many=True, context={'have_more': have_more})
            return Response(response_success(serializer.data), status=200)
        except Exception as e:
            return Response(response_error(str(e)), status=400)

    def delete(self, request, pk):
        message_id = request.GET.get('message')
        try:
            message = self.queryset.get(id=message_id, sender=request.user)
            message.delete()
            return Response(response_success("Delete successful."), status=200)
        except Exception as e:
            return Response(response_error(str(e)), status=400)

    def post(self, request, pk):
        request_copy = request.data.copy()
        request_copy['sender'] = request.user.id
        request_copy['receiver'] = pk

        serializer = MessageSerializer(data=request_copy, context={'have_more': False})
        if serializer.is_valid():
            serializer.save()
            return Response(response_success(serializer.data), status=201)
        else:
            return Response(response_error(serializer.errors), status=400)
