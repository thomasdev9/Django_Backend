from django.db import models


def upload_path(instance, filename):
    return '/'.join(['avatars', str(instance.lastname), filename])

def upload_path_post(instance, filename):
    return '/'.join(['posts', filename])

def upload_path_jobs(instance, filename):
    return '/'.join(['jobs', filename])

# Create your models here.
class UserProfile(models.Model):
    firstname = models.TextField(max_length=20, blank=False, null=False)
    lastname = models.TextField(max_length=20, blank=False, null=False)
    password = models.TextField(max_length=20, blank=False, null=False)
    email = models.TextField(max_length=35, blank=False, null=False, unique=True)
    phone = models.TextField(max_length=20, blank=False, null=False)
    image = models.ImageField(blank=True, null=True, upload_to=upload_path)

class Simple(models.Model):
    text = models.CharField(max_length=20)
    number = models.IntegerField(null=True)
    url = models.URLField(default="www.default.com")

    def __str__(self):
        return self.url

class DateExample(models.Model):
    the_data = models.DateTimeField()

class NullExample(models.Model):
    col = models.CharField(max_length=10, blank=True, null=True)

class Language(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Framework(models.Model):
    name = models.CharField(max_length=10)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=10)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name

class Post(models.Model):
    text = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=upload_path_post)
    video = models.FileField(blank=True, null=True, upload_to=upload_path_post)
    audio = models.FileField(blank=True, null=True, upload_to=upload_path_post)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)

class FriendList(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(UserProfile, blank=True, related_name='friends')

    def __str__(self):
        return self.user.lastname

    def add_friend(self, account):
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        """
        Remove friend
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Initiate the action of unfriending someone.
        """
        remover_friends_list = self # person terminating the friendship
        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)
        # Remove friend from removee's friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_frined(self, friend):
        """
        Is this a friend?
        """
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    """
    A friend request consists of two main parts:
        1.SENDER:
            -Person sending/initiating the friend request
        2.RECEIVER:
            -Person receiving the friend request.
    """
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.lastname

    def accept(self):
        """
        Accept a friend request
        Update both SENDER and RECEIVER friend list
        """
        receiver_friend_list = FriendList.objects.filter(user_id=self.receiver_id)
        sender_friend_list = FriendList.objects.filter(user_id=self.sender_id)
        if(receiver_friend_list.exists()):
            receiver_friend_list = receiver_friend_list[0]
        else:
            receiver_friend_list = FriendList.objects.create(user_id=self.receiver_id)

        if(sender_friend_list.exists()):
            sender_friend_list = sender_friend_list[0]
        else:
            sender_friend_list = FriendList.objects.create(user_id=self.sender_id)

        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender_id)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver_id)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline a friend request
        It is declined by the setting the 'is active' field to False
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request
        It is 'cancelled' by setting the 'is_active' field to False.
        """
        self.is_active = False
        self.save()

class Job(models.Model):

    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to=upload_path_jobs)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(UserProfile, related_name='participants_list', blank=True)

class ParticipantsList(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='job')
    candidates = models.ManyToManyField(UserProfile, blank=True, related_name='candidates')

    def is_candidate(self, seeker):
        if seeker in self.candidates.all():
            return True
        else:
            return False

    def add_candidate(self, seeker):
        if seeker not in self.candidates.all():
            self.candidates.add(seeker)
            self.save()
            return True
        else:
            return False

class PersonalData(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    profession = models.CharField(max_length=100)
    professional_experience = models.CharField(max_length=2000)
    education = models.CharField(max_length=2000)
    skills = models.CharField(max_length=2000)
    state_profession = models.BooleanField(default=True)
    state_experience = models.BooleanField(default=True)
    state_education = models.BooleanField(default=True)
    state_skills = models.BooleanField(default=True)

class Conversation(models.Model):
    member_1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='member_1')
    member_2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='member_2')

class Message(models.Model):
    message = models.CharField(max_length=400)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender_user')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver_user')
    date = models.DateTimeField(auto_now_add=True)

class MessageList(models.Model):
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name='conversation')
    messages = models.ManyToManyField(Message, blank=True, related_name='messages')

class Notification(models.Model):
    text = models.CharField(max_length=400)
    sender_note = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender_note')
    receiver_note = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver_note')
    date = models.DateTimeField(auto_now_add=True)