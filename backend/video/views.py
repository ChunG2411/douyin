from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import (VideoSerializer,
                          MusicSerializer,
                          LikeVideoSerializer,
                          LikeCommentSerializer,
                          CommentVideoSerializer,
                          SaveSerializer)



# Create your views here.
