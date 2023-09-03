from django.urls import path
from user.views import (
    UserRegisterView,
    UserDetailView, ModifyUser,
    LoginView, LogoutView,
    user_online, user_offline,
    UserVideoView, UserLikeVideoView, UserSaveVideoView, delete_video
)
from video.views import (
    MusicView,
    get_videolist_of_music,
    LikeVideoView,
    CommentView,
    CommentVideoView,
    DeleteCommentView,
    LikeCommentView,
    SaveVideoView
)

urlpatterns = [
    path('user/register', UserRegisterView.as_view(), name="user-register"),
    path('user/<str:username>', UserDetailView.as_view(), name="user-detail"),
    path("user/modify/<str:pk>", ModifyUser, name="user-modify"),

    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('online/<str:username>', user_online),
    path('offline/<str:username>', user_offline),

    path('user/<str:username>/video', UserVideoView.as_view(), name="user-video"),
    path('user/<str:username>/like', UserLikeVideoView.as_view(), name="user-like"),
    path('user/<str:username>/save', UserSaveVideoView.as_view(), name="user-save"),
    path('user/<str:username>/video/<str:pk>', delete_video, name="user-delete-video"),

    path('music/<str:pk>', MusicView.as_view(), name="music"),
    path('music/<str:pk>/video', get_videolist_of_music, name="music-video-list"),

    path('video/<str:pk>/save', SaveVideoView, name="video-save"),
    path('video/<str:pk>/like', LikeVideoView, name="video-like"),
    path('video/<str:pk>/comment', CommentVideoView, name="video-comment"),
    path('video/<str:pk>/comment-list', CommentView, name="video-comment-view"),

    path('comment/<str:pk>', DeleteCommentView, name="delete-comment"),
    path('comment/<str:pk>/like', LikeCommentView, name="like-comment"),

]
