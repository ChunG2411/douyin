from django.contrib import admin
from .models import User, UserFollower, UserFollowed
# Register your models here.
admin.site.register(User)
admin.site.register(UserFollower)
admin.site.register(UserFollowed)
