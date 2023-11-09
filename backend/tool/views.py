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
from .models import SearchRecent, Noti, Chat, Message, Setup
from .serializers import NotiSerializer, ChatSerializer, MessageSerializer, SetupSerializer

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

    videos = Video.objects.filter(descrip__icontains=text)[
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

    users = User.objects.exclude(id=request.user.id).filter(Q(first_name__icontains=text) | Q(
        last_name__icontains=text) | Q(username__icontains=text))[(int(page)*10):(int(page)+1)*10]
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
        member__id=request.user.id, partner__icontains=text)
    serializer = ChatSerializer(chats, many=True, context={'request': request})
    return Response(response_success(serializer.data), status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def SearchMessage(request, pk):
    text = request.query_params['text']
    try:
        chat = Chat.objects.get(id=pk)
        message = Message.objects.filter(
            receiver=chat, context__icontains=text)
        serializers = MessageSerializer(
            message, many=True, context={'have_more': False})
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
        page = request.GET.get('page')
        if not page:
            page = "0"

        chats = self.queryset.filter(member__id=request.user.id)[
            (int(page)*10):((int(page)+1)*10)]
        return Response(response_success(self.serializer_class(chats, many=True,  context={'request': request}).data), status=200)

    def delete(self, request):
        chat_id = request.GET.get('id')
        try:
            self.queryset.get(id=chat_id).delete()
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

        serializer = self.serializer_class(
            data=request_copy, context={'request': request})
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
                chat.partner = name
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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def exit_chat(request, pk):
    try:
        chat = Chat.objects.get(id=pk)
        if chat.type == "1":
            return Response(response_error("Couldn't exit this chat."), status=400)

        if request.user == chat.user:
            for i in chat.member.all():
                if i != request.user:
                    chat.user = i
                    chat.save()
                    chat.member.remove(request.user)
                    break
        else:
            chat.member.remove(request.user)

        return Response(response_success("Exit chat successful."), status=200)
    except Exception as e:
        return Response(response_error(str(e)), status=400)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def change_key_chat(request, pk):
    username = request.data.get('username')
    try:
        chat = Chat.objects.get(id=pk)
        if chat.type == "1":
            return Response(response_error("Couldn't change key of chat"), status=400)

        user = User.objects.get(username=username)
        if not user in chat.member.all():
            return Response(response_error("Check username"), status=400)

        chat.user = user
        chat.save()

        return Response(response_success("Change key of chat successful."), status=200)
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

            serializer = self.serializer_class(
                message, many=True, context={'have_more': have_more})
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

        serializer = MessageSerializer(
            data=request_copy, context={'have_more': False})
        if serializer.is_valid():
            serializer.save()
            return Response(response_success(serializer.data), status=201)
        else:
            return Response(response_error(serializer.errors), status=400)


@permission_classes([permissions.IsAuthenticated])
class SaveSetup(APIView):
    def get(self, request):
        setup = Setup.objects.get_or_create(user=request.user)[0]
        serializer = SetupSerializer(setup)
        return Response(response_success(serializer.data), status=200)

    def put(self, request):
        lang = request.data.get('lang')
        theme = request.data.get('theme')

        setup = Setup.objects.get_or_create(user=request.user)[0]
        if lang:
            setup.lang = lang
        if theme:
            setup.theme = theme
        setup.save()
        serializer = SetupSerializer(setup)

        return Response(response_success(serializer.data), status=201)
