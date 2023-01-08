from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.conf import settings
from django.utils import timezone


def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
    upload_to=user_directory_path, default='user/avatar.jpg')
    bio = models.TextField(max_length=500, blank=True)


    def clean(self):
        if not self.avatar:
            raise ValidationError("x")
        else:
            w, h = get_image_dimensions(self.avatar)
            if w != 200:
                raise ValidationError("x")
            if h != 200:
                raise ValidationError("x")

    def __str__(self):
        return self.user.username


@ receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self, removee):
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(remover_friends_list.user)

    def is_mutual(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", default=True)
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()
