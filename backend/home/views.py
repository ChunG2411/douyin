from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from social_network.config import response_error, response_success
from user.models import UserFollowed
from video.models import Video
from video.serializers import VideoSerializer
from tool.models import Chat

# Create your views here.

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def home_followed(request):
    try:
        page = request.GET.get('page')
        if not page:
            page = "0"
        
        user_followed = UserFollowed.objects.get(user=request.user)
        list_followed = user_followed.followed.values_list('id', flat=True)

        videos = Video.objects.filter(user__in=list(list_followed))[(int(page)*5):(int(page)+1)*5]
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(response_success(serializer.data), status=200)
    
    except Exception as e:
        return Response(response_error(str(e)), status=400)
    
    