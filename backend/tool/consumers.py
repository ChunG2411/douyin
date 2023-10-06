from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

import json

from .models import Noti, Chat
from user.models import User
from video.models import Video
from .serializers import NotiSerializer


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
        except: user = None
        try:
            video = Video.objects.get(id=data_json['video'])
        except: video = None
        try:
            type = data_json['type']
        except: type = None
        
        try:
            noti = Noti.objects.filter(video=video, type=type).first()
            if noti:
                if noti.status:
                    context = []
                    context.append(user.username)
                    noti = Noti.objects.create(user=video.user, video=video, type=type, context=context)
                else:
                    if user.username not in noti.context:
                        noti.context.append(user.username)
                        noti.save()
                    else:
                        pass
            else:
                context = []
                context.append(user.username)
                noti = Noti.objects.create(user=video.user, video=video, type=type, context=context)
            
            serializer = NotiSerializer(noti)
            data = {
                'id':noti.id,
                'type':noti.type,
                'status':noti.status,
                'context':noti.context,
                'create_time':noti.create_time,
                'user_id':noti.user_id,
                'video_id'
            }
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'noti',
                    'data': json.dumps(serializer.data)
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
            sender = User.objects.get(id=data_json['sender'])
            receiver = Chat.objects.get(id=data_json['receiver'])
            member = receiver.member.values_list('username', flat=True)

            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'chat',
                    'data': {
                        'sender': sender.username,
                        'receiver': receiver.id,
                        'member': list(member)
                    }
                }
            )
        except:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'chat',
                    'data': None
                }
            )
    
    def chat(self, e):
        self.send(text_data=json.dumps(e, default=str))
        

