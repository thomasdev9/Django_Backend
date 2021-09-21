from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import UserProfileViewSet, Login, UserData, CreatePost, SendPosts, NetworkData, SendFriendRequest, GetFriendRequests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register('users', UserProfileViewSet)

urlpatterns = [
    path('login/', Login.as_view()),
    path('user-data/', UserData.as_view()),
    path('create-post/', CreatePost.as_view()),
    path('send-posts/', SendPosts.as_view()),
    path('network-users/', NetworkData.as_view()),
    path('friend-request/', SendFriendRequest.as_view()),
    path('get-friend-requests/', GetFriendRequests.as_view()),
    path('', include(router.urls)),
]