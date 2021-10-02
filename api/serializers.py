from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import UserProfile, Post, FriendRequest, Job, Message, Like, Comment, Notification, PersonalData

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'firstname', 'lastname', 'password', 'email', 'phone', 'image']

class CreatePostSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100, required=True, allow_null=True, allow_blank=True)
    image = serializers.ImageField(required=True, allow_null=True, allow_empty_file=True)
    audio = serializers.FileField(required=True, allow_null=True, allow_empty_file=True)
    video = serializers.FileField(required=True, allow_null=True, allow_empty_file=True)
    email = serializers.CharField(max_length=100)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'video', 'audio', 'created_at', 'user_id']

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

class JobSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    brand = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    image = serializers.ImageField(required=True, allow_null=True, allow_empty_file=True)

class JobModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'brand', 'location', 'job_description', 'image', 'user_id', 'date']

class ApplyJobSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100, required=True)
    job_id = serializers.IntegerField(required=True)

class JobIdSerializer(serializers.Serializer):
    job_id = serializers.IntegerField(required=True)

class SettingsSerializer(serializers.Serializer):
    old_email = serializers.CharField(max_length=100, required=True)
    new_email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)
    
class PerosnalDataSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    profession = serializers.CharField(max_length=100)
    professional_experience = serializers.CharField(max_length=2000)
    education = serializers.CharField(max_length=2000)
    skills = serializers.CharField(max_length=2000)
    state_profession = serializers.BooleanField(required=True)
    state_experience = serializers.BooleanField(required=True)
    state_education = serializers.BooleanField(required=True)
    state_skills = serializers.BooleanField(required=True)

class MembersSerializer(serializers.Serializer):
    member_1 = serializers.CharField(max_length=100)
    member_2 = serializers.CharField(max_length=100)

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message','date','receiver','sender_id', 'receiver_id']

class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=400)
    sender = serializers.CharField(max_length=100)
    receiver = serializers.CharField(max_length=100)

class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post_id', 'user_id']

class GetLikeSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    post_id = serializers.IntegerField(required=True)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post_id', 'user_id']

class SendCommentSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    post_id = serializers.IntegerField(required=True)
    text = serializers.CharField(max_length=1000)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id','text','date','receiver_note_id','sender_note_id']

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = '__all__'