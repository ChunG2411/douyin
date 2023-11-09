from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

import json

from .models import Noti, Chat, Message
from user.models import User
from video.models import Video, CommentVideo


class NotiConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'notification'

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)

        try:
            user = User.objects.get(username=data_json['user'])
        except:
            user = None
        try:
            video = Video.objects.get(id=data_json['video'])
        except:
            video = None
        try:
            type = data_json['type']
        except:
            type = None

        try:
            if type == "1" or type == "2":
                user_receive = video.user
            elif type == "3":
                comment = CommentVideo.objects.get(id=data_json['comment'])
                user_receive = comment.user
            elif type == "4":
                comment = CommentVideo.objects.get(id=data_json['comment'])
                user_receive = comment.user
            elif type == "5":
                user_receive = User.objects.get(username=data_json['user_receive'])

            noti = Noti.objects.filter(user=user_receive, video=video, type=type).first()
            if noti:
                if noti.status:
                    user_interact = user.username
                    context = user.get_full_name

                    noti = Noti.objects.create(user=user_receive,
                                               video=video,
                                               type=type,
                                               user_interact=user_interact,
                                               context=context,
                                               user_send=user)
                else:
                    user_interact_list = noti.user_interact.split(',')
                    if user.username not in user_interact_list:
                        noti.user_interact += ',' + user.username
                        noti.context = user.get_full_name
                        noti.save()
                    else:
                        pass
            else:
                user_interact = user.username
                context = user.get_full_name

                noti = Noti.objects.create(user=user_receive,
                                           video=video,
                                           type=type,
                                           user_interact=user_interact,
                                           context=context,
                                           user_send=user)

            data = {
                'id': str(noti.id),
                'type': noti.type,
                'status': noti.status,
                'context': noti.context,
                'user_interact': noti.user_interact,
                'create_time': str(noti.create_time.date()) + ' ' + str(noti.create_time.time()),
                'user': str(noti.user.id),
                'video': str(noti.video.video.url) if noti.video else '',
                'user_send': str(noti.user_send.username),
                'avatar': str(noti.user_send.avatar.url)
            }
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'noti',
                    'data': data
                }
            )
        except Exception as e:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'noti',
                    'data': None
                }
            )

    def noti(self, e):
        self.send(text_data=json.dumps(e, default=str))


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'chat'

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        try:
            sender = User.objects.get(username=data_json['sender'])
            receiver = Chat.objects.get(id=data_json['receiver'])
            member = receiver.member.values_list('username', flat=True)

            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'chat',
                    'data': {
                        'sender': sender.username,
                        'receiver': {
                            'avatar': receiver.avatar.url if receiver.type=='2' else sender.avatar.url,
                            'name': receiver.name if receiver.type=='2' else sender.get_full_name
                        },
                        'member': list(member),
                        'text': sender.get_full_name + ': ' + data_json['content']
                    }
                }
            )
        except Exception as e:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'chat',
                    'data': None
                }
            )

    def chat(self, e):
        self.send(text_data=json.dumps(e, default=str))


class MessageConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'message'

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        try:
            message = Message.objects.first()

            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    "type": "message",
                    "data": {
                            "id": str(message.id),
                            "context": message.context,
                            "media": message.media.url if message.media else '',
                            "create_time": str(message.create_time.date()) + ' ' + str(message.create_time.time()),
                            "sender": str(message.sender.id),
                            "receiver": str(message.receiver.id),
                            "reader": [
                                str(message.sender.id)
                            ]
                    }
                }
            )
        except Exception as e:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'message',
                    'data': None
                }
            )

    def message(self, e):
        self.send(text_data=json.dumps(e, default=str))
