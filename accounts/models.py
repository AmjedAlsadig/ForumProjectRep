from django.db import models
from django.contrib.auth.models import User
import os, random
# Create your models here.
def get_filename_and_ext(filename):
    base_name = os.path.basename(filename)
    name ,ext = os.path.splitext(base_name)
    return name,ext
def upload_file_to_user(instance, filename):
    new_filename = random.randint(1,29494923)
    name, ext = get_filename_and_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'profile_image/{new_filename}/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)
def upload_file_to_user_cover(instance, filename):
    new_filename = random.randint(1,29494923)
    name, ext = get_filename_and_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'profile_image/cover/{new_filename}/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)

class UserProfile(models.Model):
    username = models.CharField(max_length=20)
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to=upload_file_to_user, null=True, blank=True)
    cover = models.ImageField(upload_to=upload_file_to_user_cover, null=True, blank=True)
    def __str__(self):
        return self.user.username

class Friend(models.Model):
    friend_list = models.ManyToManyField(UserProfile)
    current_user = models.ForeignKey(UserProfile,related_name='account_owner', null=True)
    following = models.ManyToManyField(UserProfile,related_name='following')
    @classmethod 
    def follow(cls,user_following ,user_to_follow):
        user, created = cls.objects.get_or_create(current_user = user_following)
        user.following.add(user_to_follow)
    @classmethod 
    def un_follow(cls,user_following ,user_to_unfollow):
        user, created = cls.objects.get_or_create(current_user = user_following)
        user.following.remove(user_to_unfollow)
    @classmethod 
    def add_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user = current_user)
        friend.friend_list.add(new_friend)
        friend_bidrec, created = cls.objects.get_or_create(current_user = new_friend)
        friend_bidrec.friend_list.add(current_user)
    @classmethod 
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user = current_user)
        friend.friend_list.remove(new_friend)
        friend_bidrec, created = cls.objects.get_or_create(current_user = new_friend)
        friend_bidrec.friend_list.remove(current_user)
class FriendRequest(models.Model):
    sender = models.ForeignKey(UserProfile,related_name='request_sender')
    receiver = models.ForeignKey(UserProfile, related_name='request_receiver')
    requested = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True)
    delete =  models.BooleanField(default=False)