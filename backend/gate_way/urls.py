from django.urls import path

from user.views import (
    UserRegisterView,
    UserDetailView, ModifyUser, GetMyProfile,
    LoginView, LogoutView,
    user_online, user_offline,
    UserVideoView, UserLikeVideoView, UserSaveVideoView, delete_video, FollowView,
    GetUserFollowed, GetUserFollower
)
from video.views import (
    MusicView, MusicDetailView, get_my_music,
    get_videolist_of_music,
    get_video,
    LikeVideoView,
    CommentView,
    CommentVideoView,
    DeleteCommentView,
    LikeCommentView,
    SaveVideoView
)
from tool.views import (
    SearchVideo, SearchUser, SearchChat, SearchMessage, RecentSearch, SuggestSearch,
    NotiView, DeleteNotiView,
    ChatView,
    MessageView,
    add_member_to_chat, remove_member_to_chat,
    testview
)

urlpatterns = [
    path('user/self', GetMyProfile, name="self"),
    path('user/register', UserRegisterView.as_view(), name="user-register"),
    path('user/<str:username>', UserDetailView.as_view(), name="user-detail"),
    path("user/modify/<str:pk>", ModifyUser, name="user-modify"),

    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('online', user_online, name="online"),
    path('offline', user_offline, name="offline"),

    path('user/<str:username>/video', UserVideoView.as_view(), name="user-video"),
    path('user/<str:username>/like', UserLikeVideoView.as_view(), name="user-like"),
    path('user/<str:username>/save', UserSaveVideoView.as_view(), name="user-save"),
    path('user/<str:username>/video/<str:pk>', delete_video, name="user-delete-video"),
    path('user/<str:username>/follow', FollowView, name="user-follow"),
    path('user/<str:username>/followed-list', GetUserFollowed, name="user-followed-list"),
    path('user/<str:username>/follower-list', GetUserFollower, name="user-follower-list"),

    path('music', MusicView.as_view(), name="music"),
    path('music/self', get_my_music, name="music-self"),
    path('music/<str:pk>', MusicDetailView.as_view(), name="music-detail"),
    path('music/<str:pk>/video', get_videolist_of_music, name="music-video-list"),

    path('video/<str:pk>', get_video, name="video"),
    path('video/<str:pk>/save', SaveVideoView, name="video-save"),
    path('video/<str:pk>/like', LikeVideoView, name="video-like"),
    path('video/<str:pk>/comment', CommentVideoView, name="video-comment"),
    path('video/<str:pk>/comment-list', CommentView, name="video-comment-view"),

    path('comment/<str:pk>', DeleteCommentView, name="delete-comment"),
    path('comment/<str:pk>/like', LikeCommentView, name="like-comment"),

    path('search/video', SearchVideo, name="search-video"),
    path('search/user', SearchUser, name="search-user"),
    path('search/chat', SearchChat, name="search-chat"),
    path('search/chat/<str:pk>/message', SearchMessage, name="search-message"),
    path('search/recent', RecentSearch, name="search-recent"),
    path('search/suggest', SuggestSearch, name="search-suggest"),

    path('notification', NotiView, name="noti"),
    path("notification/<str:pk>", DeleteNotiView, name="noti-delete"),

    path("chat", ChatView.as_view(), name="chat"),
    path("chat/<str:pk>/detail", MessageView.as_view(), name="message"),
    path("chat/<str:pk>/add", add_member_to_chat, name="chat-add"),
    path("chat/<str:pk>/remove", remove_member_to_chat, name="chat-remove"),

    path('test', testview)
]
