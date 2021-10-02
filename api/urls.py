from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import UserProfileViewSet, Login, UserData, CreatePost, SendPosts, NetworkData, SendFriendRequest, GetFriendRequests, AcceptFriendRequest, DeclineFriendRequest, CreateJob, GetJobs, GetMyJobs, ApplyJob, GetParticipants, ChangeData, SendPersonalData, GetConversation, GetFriends, SendMessage, GetId, GetUserFromId, GetAllUsers, GetLikes, SendLike, SendComment, GetComments, GetNotifications, GetData, Register
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
    path('accept-friend-request/', AcceptFriendRequest.as_view()),
    path('decline-friend-request/', DeclineFriendRequest.as_view()),
    path('create-job/', CreateJob.as_view()),
    path('get-jobs/', GetJobs.as_view()),
    path('get-my-jobs/', GetMyJobs.as_view()),
    path('apply-job/', ApplyJob.as_view()),
    path('get-participants/', GetParticipants.as_view()),
    path('change-data/', ChangeData.as_view()),
    path('personal-data/', SendPersonalData.as_view()),
    path('get-conversation/', GetConversation.as_view()),
    path('get-friends/', GetFriends.as_view()),
    path('send-message/', SendMessage.as_view()),
    path('get-id/', GetId.as_view()),
    path('get-user/', GetUserFromId.as_view()),
    path('get-all-users/', GetAllUsers.as_view()),
    path('get-likes/', GetLikes.as_view()),
    path('send-like/', SendLike.as_view()),
    path('send-comment/', SendComment.as_view()),
    path('get-comments/', GetComments.as_view()),
    path('get-notifications/', GetNotifications.as_view()),
    path('get-data/', GetData.as_view()),
    path('register/', Register.as_view()),
    path('', include(router.urls)),
]