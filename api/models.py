from django.db import models


def upload_path(instance, filename):
    return '/'.join(['avatars', str(instance.lastname), filename])

def upload_path_post(instance, filename):
    return '/'.join(['posts', filename])

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
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
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
