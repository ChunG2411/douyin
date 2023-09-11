from django.contrib import admin
from .models import Noti, SingleChat, Group, GroupChat
# Register your models here.
admin.site.register(Noti)
admin.site.register(SingleChat)
admin.site.register(Group)
admin.site.register(GroupChat)
