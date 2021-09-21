from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, PostSerializer, CreatePostSerializer, EmailSerializer, FriendRequestSerializer, ReuqestSerializer
from django.http import HttpResponse
from .models import UserProfile, Post, FriendRequest

class Login(APIView):

    def get(self, request):
        user = UserProfile.objects.all()
        serializer = UserProfileSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = UserProfile.objects.filter(email=email, password=password)
        serializer = UserProfileSerializer(user, many=True)
        return Response(serializer.data)

class PostData(APIView):

    def get(self, request):
        pass

    def post(self, request):
        email = request.data['email']
        posts = Post.objects.filter(user__email=email)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class UserData(APIView):

    def get(self, request):
        pass

    def post(self, request):
        email = request.data['email']
        user = UserProfile.objects.filter(email=email)
        serializer = UserProfileSerializer(user, many=True)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request, args, **kwargs):
        firstname = request.data['firstname']
        lastname = request.data['lastname']
        password = request.data['password']
        email = request.data['email']
        phone = request.data['phone']
        image = request.data['image']
        UserProfile.objects.create(firstname=firstname, lastname=lastname, password=password, email=email, phone=phone, image=image)
        return HttpResponse({'message': 'User created'}, status=200)

class CreatePost(APIView):

    def post(self, request):
        serializer = CreatePostSerializer(data=request.data)
        text = serializer.initial_data.get('text')
        image = serializer.initial_data.get('image')
        video = serializer.initial_data.get('video')
        audio = serializer.initial_data.get('audio')
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        Post.objects.create(text=text, image=image, video=video, audio=audio, user_id=user_id)
        return Response({'Message': 'Post created'}, status=200)

class SendPosts(APIView):

    def get(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        posts = Post.objects.filter(user__email=email).order_by('-created_at')
        postSerializer = PostSerializer(posts, many=True)
        return Response(postSerializer.data)

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        posts = Post.objects.filter(user__email=email).order_by('-created_at')
        postSerializer = PostSerializer(posts, many=True)
        return Response(postSerializer.data)

class NetworkData(APIView):

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        users = UserProfile.objects.exclude(email=email)
        usersSerializer = UserProfileSerializer(users, many=True)
        return Response(usersSerializer.data)

class SendFriendRequest(APIView):

    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        sender = serializer.initial_data.get('sender')
        receiver = serializer.initial_data.get('receiver')
        user_sender = UserProfile.objects.get(email=sender)
        user_receiver = UserProfile.objects.get(email=receiver)
        sender_id = user_sender.id
        receiver_id = user_receiver.id
        FriendRequest.objects.create(sender_id=sender_id, receiver_id=receiver_id)
        return Response({'Message': 'Friend Request sent'}, status=200)

class GetFriendRequests(APIView):

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        requests = FriendRequest.objects.filter(receiver_id=user_id, is_active=True)
        requests_id = []
        for req in requests:
            requests_id.append(req.sender_id)
        users = UserProfile.objects.filter(pk__in=requests_id)
        userData = UserProfileSerializer(users, many=True)
        return Response(userData.data)

