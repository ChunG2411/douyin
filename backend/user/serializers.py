from rest_framework import serializers

from .models import User, UserFollower, UserFollowed
from video.models import Video
from social_network.config import response_error

class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        gender = request.data.get('gender')
        password = request.data.get('password')

        # check gender
        avatar = None
        if gender:
            if gender == "Male":
                # validated_data['gender'] = "Male"
                avatar = "template/male.jpg"
            elif gender == "Female":
                # validated_data['gender'] = "Female"
                avatar = "template/female.jpg"
            elif gender == "Other":
                # validated_data['gender'] = "Other"
                avatar = "template/other.jpg"
            else:
                raise serializers.ValidationError(response_error("Gender must in [M, F, O]."))
        else:
            raise serializers.ValidationError(response_error("Gender must in [M, F, O]."))
        
        # check password
        if len(password) < 6:
            raise serializers.ValidationError(response_error("Password must be at least 6 characters."))
        
        password_split = [*password]
        if ord(password_split[0]) not in range(65, 90):
            raise serializers.ValidationError(response_error("The first letter of the password must be capitalized."))
        check_have_number = False
        for i in password_split:
            if ord(i) in range(48, 57):
                check_have_number = True
                break
        if not check_have_number:
            raise serializers.ValidationError(response_error("Password must contain number."))
        validated_data['password'] = password

        user = User(**validated_data)
        user.avatar = avatar
        user.set_password(password)
        user.save()

        UserFollower.objects.create(user=user)
        UserFollowed.objects.create(user=user)

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    followed_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }
    
    def get_followed_count(self, obj):
        followed = UserFollowed.objects.get(user=obj)
        return followed.followed_count

    def get_follower_count(self, obj):
        follower = UserFollower.objects.get(user=obj)
        return follower.follower_count

    def get_video_count(self, obj):
        video = Video.objects.filter(user=obj)
        return video.count()

    def get_full_name(self, obj):
        return obj.get_full_name
    