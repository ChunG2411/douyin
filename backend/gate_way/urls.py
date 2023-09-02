from django.urls import path
from user.views import (
    UserRegisterView,
    UserDetailView, ModifyUser,
    LoginView, LogoutView,
    user_online, user_offline,
    UserVideoView, UserLikeVideoView, UserSaveView
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
    path('user/<str:username>/save', UserSaveView.as_view(), name="user-save"),

]
