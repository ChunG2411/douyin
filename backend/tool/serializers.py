from rest_framework import serializers

from .models import Noti


class NotiSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Noti
        fields = "__all__"
    
    def get_type(self, obj):
        return obj.get_type_display()
    
