from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from itertools import chain
from .serializers import UserProfileSerializer, PostSerializer, CreatePostSerializer, EmailSerializer, FriendRequestSerializer, ReuqestSerializer, JobSerializer, JobModelSerializer, ApplyJobSerializer, JobIdSerializer, SettingsSerializer, PerosnalDataSerializer, MembersSerializer, MessageSerializer, SendMessageSerializer, IdSerializer, LikeSerializer, GetLikeSerializer, CommentSerializer, SendCommentSerializer, NotificationSerializer, DataSerializer
from django.http import HttpResponse
import json
from .models import UserProfile, Post, FriendRequest, Job, ParticipantsList, PersonalData, Conversation, Message, MessageList, FriendList, Like, Comment, Notification

class Login(APIView):

    def get(self, request):
        user = UserProfile.objects.all()
        serializer = UserProfileSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = UserProfile.objects.filter(email=email, password=password)
        if user.exists():
            serializer = UserProfileSerializer(user, many=True)
            return Response(serializer.data)
        else:
            return Response({'Message': 'This user does not exist.'},status=200)


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

class Register(APIView):

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        firstname = serializer.initial_data.get('firstname')
        lastname = serializer.initial_data.get('lastname')
        password = serializer.initial_data.get('password')
        email = serializer.initial_data.get('email')
        phone = serializer.initial_data.get('phone')
        image = serializer.initial_data.get('image')
        user = UserProfile.objects.filter(email=email)
        if user.exists():
            return Response({'Message': 'This email is token'}, status=200)
        else:
            UserProfile.objects.create(firstname=firstname, lastname=lastname, password=password, email=email,
                                       phone=phone, image=image)
            return HttpResponse({'Message': 'User created'}, status=200)

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
        user = UserProfile.objects.filter(email=email)
        if user.exists():
            return Response({'Message': 'This email is token'}, status=200)
        else:
            UserProfile.objects.create(firstname=firstname, lastname=lastname, password=password, email=email,
                                       phone=phone, image=image)
            return Response({'Message': 'User created'}, status=200)


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
        post = Post.objects.create(text=text, image=image, video=video, audio=audio, user_id=user_id)
        serializer_post = PostSerializer(post)
        return Response(serializer_post.data)

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
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        posts = Post.objects.filter(user__email=email).order_by('-created_at')
        my_posts = Post.objects.filter(user__email=email)
        friend_list = FriendList.objects.filter(user_id=user_id)
        if friend_list.exists():
            friend_list = friend_list[0]
            friend_list_id = []
            friends = friend_list.friends.all()
            for friend in friends:
                friend_list_id.append(friend.id)
            friend_posts = Post.objects.filter(user_id__in = friend_list_id)
            print(friend_posts)
            friend_likes = Like.objects.filter(user_id__in=friend_list_id)
            if friend_likes.exists():
                post_likes_id = []
                for like in post_likes_id:
                    post_likes_id.append(like.post_id)
                post_friends_likes = Post.objects.filter(id__in=post_likes_id)
                print(post_friends_likes)
        post_list = sorted(
            chain(my_posts, friend_posts, post_friends_likes),
            key=lambda instance: instance.created_at)
        print(post_list)
        postSerializer = PostSerializer(post_list, many=True)
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

class AcceptFriendRequest(APIView):

    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        sender = serializer.initial_data.get('sender')
        receiver = serializer.initial_data.get('receiver')
        sender_id = UserProfile.objects.get(email=sender)
        receiver_id = UserProfile.objects.get(email=receiver)
        friend_request = FriendRequest.objects.get(receiver_id=receiver_id, sender_id=sender_id, is_active=True)
        friend_request.accept()
        return Response({'Message': 'Friend Request was accepted'}, status=200)

class DeclineFriendRequest(APIView):

    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        sender = serializer.initial_data.get('sender')
        receiver = serializer.initial_data.get('receiver')
        sender_id = UserProfile.objects.get(email=sender)
        receiver_id = UserProfile.objects.get(email=receiver)
        friend_request = FriendRequest.objects.get(receiver_id=receiver_id, sender_id=sender_id, is_active=True)
        friend_request.decline()
        return Response({'Message': 'Friend Request was declined'}, status=200)

class CreateJob(APIView):

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        title = serializer.initial_data.get('title')
        brand = serializer.initial_data.get('brand')
        location = serializer.initial_data.get('location')
        description = serializer.initial_data.get('description')
        image = serializer.initial_data.get('image')
        Job.objects.create(title=title, brand=brand, location=location, job_description=description, image=image, user_id=user_id)
        return Response({'Message': 'Job posted'}, status=200)

class GetJobs(APIView):

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        jobs = Job.objects.exclude(user_id=user_id)
        jobsData = JobModelSerializer(jobs, many=True)
        return Response(jobsData.data)

class GetMyJobs(APIView):

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        jobs = Job.objects.filter(user_id=user_id)
        jobsData = JobModelSerializer(jobs, many=True)
        return Response(jobsData.data)

class ApplyJob(APIView):

    def post(self, request):
        serializer = ApplyJobSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        job_id = serializer.initial_data.get('job_id')
        job = Job.objects.get(id=job_id)
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        if (job.user_id == user_id):
            return Response({'Message': 'You cannot apply for this job.'}, status=200)
        job_candidates_list = ParticipantsList.objects.filter(job_id=job_id)
        if(job_candidates_list.exists()):
            job_candidates_list = job_candidates_list[0]
        else:
            job_candidates_list = ParticipantsList.objects.create(job_id=job_id)

        if job_candidates_list.is_candidate(user):
            return Response({'Message': 'You have already applied for this job.'}, status=200)

        job_candidates_list.add_candidate(user)
        return Response({'Message': 'You applied for this job successfully.'}, status=200)

class GetParticipants(APIView):

    def post(self, request):
        serializer = ApplyJobSerializer(data=request.data)
        job_id = serializer.initial_data.get('job_id')
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        job = Job.objects.get(id=job_id)
        if(job.user_id != user_id):
            return Response({'Message': 'You cannot view the participants'}, status=200)

        job_candidates_list = ParticipantsList.objects.filter(job_id=job_id)
        if (job_candidates_list.exists()):
            job_candidates_list = job_candidates_list[0]
        else:
            job_candidates_list = ParticipantsList.objects.create(job_id=job_id)

        serializer_user = UserProfileSerializer(job_candidates_list.candidates.all(), many=True)
        return Response(serializer_user.data)

class ChangeData(APIView):

    def post(self, request):
        serializer = SettingsSerializer(data=request.data)
        old_email = serializer.initial_data.get('old_email')
        new_email = serializer.initial_data.get('new_email')
        password = serializer.initial_data.get('password')
        user = UserProfile.objects.filter(email=new_email)
        if user.exists():
            return Response({'Message': 'This email is token by another user.'}, status=200)
        else:
            user_profile = UserProfile.objects.get(email=old_email)
            user_profile.email = new_email
            user_profile.password = password
            user_profile.save()
            return Response({'Message': 'Successfully changed the settings.'}, status=200)

class SendPersonalData(APIView):

    def post(self, request):
        serializer = PerosnalDataSerializer(data=request.data)
        profession = serializer.initial_data.get('profession')
        email = serializer.initial_data.get('email')
        professional_experience = serializer.initial_data.get('professional_experience')
        education = serializer.initial_data.get('education')
        skills = serializer.initial_data.get('skills')
        state_profession = json.loads(request.POST.get('state_profession'))
        state_experience = json.loads(request.POST.get('state_experience'))
        state_education = json.loads(request.POST.get('state_education'))
        state_skills = json.loads(request.POST.get('state_skills'))
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        personal_data = PersonalData.objects.filter(user_id=user_id)
        if personal_data.exists():
            personal_data = personal_data[0]
            personal_data.profession = profession
            personal_data.professional_experience = professional_experience
            personal_data.education = education
            personal_data.skills = skills
            personal_data.state_profession = state_profession
            personal_data.state_experience = state_experience
            personal_data.state_education = state_education
            personal_data.state_skills = state_skills
            personal_data.save()
        else:
            personal_data = PersonalData.objects.create(user_id=user_id, profession=profession, professional_experience=professional_experience, education=education, skills=skills, state_profession=state_profession, state_experience=state_experience, state_education=state_education, state_skills=state_skills)

        return Response({'Message': 'Personal Data updated'}, status=200)

class GetConversation(APIView):

    def post(self, request):
        serializer = MembersSerializer(data=request.data)
        member_1 = serializer.initial_data.get('member_1')
        member_2 = serializer.initial_data.get('member_2')
        user_1 = UserProfile.objects.get(email=member_1)
        user_2 = UserProfile.objects.get(email=member_2)
        member_1_id = user_1.id
        member_2_id = user_2.id
        conversation = Conversation.objects.filter(member_1_id=member_1_id, member_2_id=member_2_id)
        if conversation.exists():
            conversation = conversation[0]
            conversation_id = conversation.id
            message_list = MessageList.objects.filter(conversation_id=conversation_id)
            if message_list.exists():
                message_list = message_list[0]
                message_data = MessageSerializer(message_list.messages.all(), many=True)
                return Response(message_data.data)
            else:
                message_list = MessageList.objects.create(conversation_id=conversation_id)
                message_data = MessageSerializer(message_list.messages.all(), many=True)
                return Response(message_data.data)
        else:
            conversation_temp = Conversation.objects.filter(member_1_id=member_2_id, member_2_id=member_1_id)
            if conversation_temp.exists():
                conversation = conversation_temp[0]
                conversation_id = conversation.id
                message_list = MessageList.objects.filter(conversation_id=conversation_id)
                message_list = message_list[0]
            else:
                conversation = Conversation.objects.create(member_1_id=member_1_id, member_2_id=member_2_id)
                conversation_id = conversation.id
                message_list = MessageList.objects.create(conversation_id=conversation_id)
            message_data = MessageSerializer(message_list.messages.all(), many=True)
            return Response(message_data.data)

class SendMessage(APIView):

    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        member_1 = serializer.initial_data.get('member_1')
        member_2 = serializer.initial_data.get('member_2')
        text = serializer.initial_data.get('message')
        user_1 = UserProfile.objects.get(email=member_1)
        user_2 = UserProfile.objects.get(email=member_2)
        member_1_id = user_1.id
        member_2_id = user_2.id
        conversation = Conversation.objects.filter(member_1_id= member_1_id, member_2_id=member_2_id)
        if conversation.exists():
            conversation = conversation[0]
            conversation_id = conversation.id
        else:
            conversation_temp = Conversation.objects.filter(member_1_id=member_2_id, member_2_id=member_1_id)
            conversation = conversation_temp[0]
            conversation_id = conversation.id
        message_list = MessageList.objects.get(conversation_id=conversation_id)
        message = Message.objects.create(message=text, sender_id=member_1_id, receiver_id=member_2_id)
        message_list.messages.add(message)
        return Response({'Message': 'Message was sent'}, status=200)

class GetFriends(APIView):

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        friend_list = FriendList.objects.filter(user_id=user_id)
        if friend_list.exists():
            friend_list = friend_list[0]
            serializer_friends = UserProfileSerializer(friend_list.friends.all(), many=True)
            return Response(serializer_friends.data)
        else:
            return Response({'Message': 'No friends yet'}, status=200)

class GetId(APIView):
    
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        serializer_user = UserProfileSerializer(user, many=False)
        return Response(serializer_user.data)

class GetUserFromId(APIView):

    def post(self, request):
        serializer = IdSerializer(data=request.data)
        id = serializer.initial_data.get('id')
        user = UserProfile.objects.get(id=id)
        serializer_user = UserProfileSerializer(user)
        return Response(serializer_user.data)

class GetAllUsers(APIView):

    def get(self, request):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)

class GetLikes(APIView):

    def get(self, request):
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

class SendLike(APIView):

    def post(self, request):
        serializer = GetLikeSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        post_id = serializer.initial_data.get('post_id')
        post = Post.objects.get(id=post_id)
        receiver_id = post.user_id
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        like = Like.objects.filter(post_id=post_id, user_id=user_id)
        if like.exists():
            return Response({'Message': 'You have already liked this post.'}, status=200)
        else:
            Like.objects.create(post_id=post_id,user_id=user_id)
            text = ' liked your post.'
            notification = Notification.objects.create(sender_note_id=user_id,receiver_note_id=receiver_id,text=text)
            return Response({'Message': 'You liked the post.'}, status=200)

class SendComment(APIView):

    def post(self, request):
        serializer = SendCommentSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        post_id = serializer.initial_data.get('post_id')
        post = Post.objects.get(id=post_id)
        receiver_id = post.user_id
        text = serializer.initial_data.get('text')
        comment = Comment.objects.create(user_id=user_id,post_id=post_id,text=text)
        text = ' commented your post.'
        notification = Notification.objects.create(sender_note_id=user_id,receiver_note_id=receiver_id,text=text)
        return Response({'Message': 'Comment was created'}, status=200)

class GetComments(APIView):

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class GetNotifications(APIView):

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        notifications = Notification.objects.filter(receiver_note_id=user_id)
        serializer_notification = NotificationSerializer(notifications, many=True)
        return Response(serializer_notification.data)

class GetData(APIView):

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        email = serializer.initial_data.get('email')
        user = UserProfile.objects.get(email=email)
        user_id = user.id
        personal_data = PersonalData.objects.filter(user_id=user_id)
        if personal_data.exists():
            serializer_data = DataSerializer(personal_data, many=True)
            return Response(serializer_data.data)
        else:
            return Response({'data': []}, status=200)