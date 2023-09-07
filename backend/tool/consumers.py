from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

import json

from .models import Noti
from user.models import User
from video.models import Video
from .serializers import NotiSerializer


class NotiConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = 'notification'
        self.user = None

    def connect(self):
        print("check")
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
        user = User.objects.get(id=data_json['user'])
        video = Video.objects.get(id=data_json['video'])
        type = data_json['type']

        noti = Noti.objects.filter(video=video).first()
        if noti:
            if noti.status:
                context = user.last_name
                noti = Noti.objects.create(user=video.user, video=video, type=type, context=context)
            else:
                number = [int(s) for s in noti.context.split() if s.isdigit()]
                if number:
                    context = user.last_name + f"and {number+1} other user"
                else:
                    context = user.last_name + "and 1 other user"

                noti.context = context
                noti.save()
        else:
            context = user.last_name
            noti = Noti.objects.create(user=video.user, video=video, type=type, context=context)

        serializer = NotiSerializer(noti)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                'type': 'noti',
                'data': serializer.data
            }
        )

    def noti(self, e):
        self.send(text_data=json.dumps(e))
    
