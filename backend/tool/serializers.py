from rest_framework import serializers

from .models import Noti, Chat, Message
from user.models import User
from social_network.config import response_error

from datetime import datetime


class NotiSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Noti
        fields = "__all__"
    
    def get_type(self, obj):
        return obj.get_type_display()
    

class ChatSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = "__all__"
        lookup_field = "id"
    
    def get_member(self, obj):
        list_member = []
        for i in obj.member.all():
            list_member.append(i.username)
        return list_member
    
    def create(self, validated_data):
        request = self.context.get('request')
        type = request.data.get('type')
        member = request.data.get('member')

        chat = Chat(**validated_data)
        chat.last_action = datetime.now()
        if type == "1":
            for i in member:
                if i != request.user.username:
                    try:
                        user = User.objects.get(username=i)
                    except:
                        raise serializers.ValidationError(response_error("Member user don't exist."))
                    chat.avatar = user.avatar
        else:
            chat.avatar = "template/group.png"
        chat.save()
        return chat