from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.db.models.signals import pre_save
import os, random
from accounts.models import UserProfile
# Create your models here.
def get_filename_and_ext(filename):
    base_name = os.path.basename(filename)
    name ,ext = os.path.splitext(base_name)
    return name,ext
def upload_file_to(instance, filename):
    new_filename = random.randint(1,29494923)
    name, ext = get_filename_and_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'post/{new_filename}/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)
def upload_file_to_image(instance, filename):
    new_filename = random.randint(1,29494923)
    name, ext = get_filename_and_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'comment/{new_filename}/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)
class AccountManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)   #account.objects    =   self.get_queryset()
        if qs.count() == 1:
            return qs.first() 
        return None
class Post(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_file_to, null=True, blank=True)
    auther = models.ForeignKey(UserProfile)
    like_count = models.IntegerField(default=0)
    def Likes_count(self):
        try :
            b = Likes.objects.get(post=self)
            out = b.likes_list.count()
        except Likes.DoesNotExist:
            out = 0
        return out
    def comments_count(self):
        try :
            b = Comment.objects.filter(post=self).count()
            out_c = b
        except Comment.DoesNotExist:
            out_c = 0
        return out_c
    def get_absolute_url(self):
        # return "{slug}/".format(slug=self.slug)
        return reverse("posts:detail",kwargs={"slug":self.slug})
    objects  =   AccountManager()
    def __str__(self):
        return self.title
def post_pre_save_reciver(sender, instance, *arg, **kwargs):
    if not instance.slug :
        instance.slug   = unique_slug_generator(instance)
pre_save.connect(post_pre_save_reciver, sender = Post)
class Comment(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(blank=True, unique=True)
    content = models.TextField()
    post = models.ForeignKey(Post)
    time = models.DateTimeField(auto_now_add=True)
    auther = models.ForeignKey(UserProfile)
    image = models.ImageField(upload_to=upload_file_to_image, null=True, blank=True)
    class Meta:
        ordering = ['-time',]
    objects     =   AccountManager()
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"slug": self.slug})
    def __str__(self) :
         return self.title
def comment_pre_save_reciver(sender, instance, *arg, **kwargs):
    if not instance.slug :
        instance.slug   = unique_slug_generator(instance)
pre_save.connect(comment_pre_save_reciver, sender = Comment)
class Likes(models.Model):
    likes_value = models.IntegerField(default=0)
    post = models.ForeignKey(Post)
    likes_list = models.ManyToManyField(UserProfile, blank=True)
    @classmethod 
    def add_like(cls, current_post, user_like):
        like, created = cls.objects.get_or_create(post = current_post)
        like.likes_list.add(user_like)
        b = Likes.objects.get(post=current_post)
        out_x = b.likes_list.count()
    @classmethod 
    def remove_like(cls, current_post, user_like):
        like, created = cls.objects.get_or_create(post = current_post)
        like.likes_list.remove(user_like)
        b = Likes.objects.get(post=current_post)
        out_x = b.likes_list.count()
        print(out_x)
        print('removed')
class Notifications(models.Model):
    sender = models.ForeignKey(UserProfile,related_name='sender')
    receivers = models.ManyToManyField(UserProfile,related_name='receiver')
    post = models.ForeignKey(Post)
    action_type = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True)
    def read(self):
        self.read_at = now
        print(self.read_at)
    @classmethod
    def add_nofi(cls, sender,post_obj,action,receiver):
        notifications, created = cls.objects.get_or_create(
            sender=sender,
            post = post_obj,
            action_type = action
        )
        notifications.receivers.add(*receiver)
    @classmethod
    def remove_nofi(cls, sender, receiver):
        notifications, created = cls.objects.get_or_create(sender=sender)
        notifications.receivers.remove(receiver)
    
