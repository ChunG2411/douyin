from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator

from .managers import CustomUserManager

import uuid

# Create your models here.
class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=100, unique=True, validators=[username_validator], default=uuid.uuid4)
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatar')
    introduce = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def completed_fields_percent(self):
        fields = ['email', 'first_name', 'last_name', 'address', 'gender', 'birth', 'avatar', 'introduce']
        empty = ["", None]
        empty_count = 0

        for i in fields:
            fiels_value = getattr(self, i)
            if fiels_value in empty:
                empty_count += 1
        
        completed_percent = (len(fields) - empty_count)/len(fields)*100
        return f"{completed_percent:.2f}"
    
    class Meta:
        db_table = 'tb_user'
        verbose_name = 'User'


class UserStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_status")
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_user_status'
        verbose_name = 'User status'


class UserFollower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_follower")
    follower = models.ManyToManyField(User, blank=True, related_name="follower")

    class Meta:
        db_table = 'tb_user_follower'
        verbose_name = 'User Follower'

    def __str__(self):
        return self.user.username

    @property
    def follower_count(self):
        return self.follower.count()


class UserFollowed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_followed")
    followed = models.ManyToManyField(User, blank=True, related_name="followed")

    class Meta:
        db_table = 'tb_user_followed'
        verbose_name = 'User Followed'
    
    def __str__(self):
        return self.user.username
    
    @property
    def followed_count(self):
        return self.followed.count()
    
