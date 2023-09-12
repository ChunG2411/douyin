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
    type = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = "__all__"

    def get_member(self, obj):
        list_member = []
        for i in obj.member.all():
            list_member.append(i.username)
        return list_member

    def get_type(self, obj):
        return obj.get_type_display()

    def create(self, validated_data):
        member = self.initial_data['member'].replace(' ', '')
        user_id = self.initial_data['user']
        
        member_split = member.split(',')

        if len(member_split) == 1:
            try:
                user = User.objects.get(username=member_split[0])
                type = "1"
                avatar = user.avatar.url.replace('/media/', '')
                name = user.get_full_name
            except Exception as e:
                raise serializers.ValidationError(response_error(str(e)))
            
            chat = Chat.objects.filter(name=name)
            if chat:
                raise serializers.ValidationError(response_error("Chat already exist."))
        else:
            type = "2"
            avatar = "template/group.png"
            name = f"You and {len(member_split)} other people"

        request_user = User.objects.get(id=user_id)
        member_split.append(request_user.username)
        
        validated_data['type'] = type
        validated_data['name'] = name

        chat = Chat(**validated_data)
        chat.avatar = avatar
        chat.last_action = datetime.now()

        chat.save()
        for i in member_split:
            try:
                user = User.objects.get(username=i)
                chat.member.add(user)
            except Exception as e:
                chat.delete()
                raise serializers.ValidationError(response_error(str(e)))
        chat.save()
        return chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

