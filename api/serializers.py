from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import UserProfile, Post, FriendRequest

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'password', 'email', 'phone', 'image']

class CreatePostSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100, required=True, allow_null=True, allow_blank=True)
    image = serializers.ImageField(required=True, allow_null=True, allow_empty_file=True)
    audio = serializers.FileField(required=True, allow_null=True, allow_empty_file=True)
    video = serializers.FileField(required=True, allow_null=True, allow_empty_file=True)
    email = serializers.CharField(max_length=100)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text', 'image', 'video', 'audio', 'created_at', 'user_id']

class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

class FriendRequestSerializer(serializers.Serializer):
    sender = serializers.CharField(max_length=100)
    receiver = serializers.CharField(max_length=100)

class ReuqestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['sender_id', 'receiver_id', 'is_active', 'timestamp']

class FriendRequestDetails(serializers.Serializer):
    sender = serializers.CharField(max_length=100)
    receiver = serializers.CharField(max_length=100)
    sender_image = serializers.ImageField(required=True, allow_null=True, allow_empty_file=True)
    sender_firstname = serializers.CharField(max_length=100)
    sender_lastname = serializers.CharField(max_length=100)