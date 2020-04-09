from django import forms
from django.contrib.auth import get_user_model
# from . import models
from .models import upload_file_to, get_filename_and_ext,  Post, Comment, Friend
from .utils import unique_slug_generator

from django.core.files.images import get_image_dimensions
from .models import UserProfile

from django.shortcuts import Http404

class friends_form(forms.ModelForm):
    class Meta :
        model   =   Friend
        fields  =   '__all__'

class post_form(forms.ModelForm):   
    class Meta:
        model   =   Post
        fields = '__all__'
        exclude = ['auther','slug','like_count']
        # fileds  =   [
        #     'title',
        #     'content'
        # ]
    # image       =   forms.ImageField(required=False)

class comment_form(forms.ModelForm):
    class Meta:
        model   =   Comment
        fields = '__all__'
        exclude = ['auther','post']


class ProfileForm(forms.Form):
    Fullname    =   forms.CharField(
        widget  = forms.TextInput(
            attrs ={
                "placeholder" : "Enter your Name"
            }
        )
    )

    Email       =   forms.EmailField(
        widget  = forms.EmailInput(
            attrs ={
                "placeholder" : "Enter your Email"
            }
        )
        )

    Password    =   forms.CharField(
        widget  = forms.PasswordInput(
            attrs ={
                "placeholder" : "Enter your Password"
            }
        )
    )

class loginForm(forms.Form):
    username    =   forms.CharField(widget=forms.TextInput)  
    password    =   forms.CharField(widget=forms.PasswordInput)
User = get_user_model()
class registerForm(forms.Form):
    username    =   forms.CharField(widget=forms.TextInput)
    email       =   forms.EmailField(widget=forms.EmailInput)
    password    =   forms.CharField(widget=forms.PasswordInput)
    password2   =   forms.CharField(widget=forms.PasswordInput,label="Confirm password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs       = User.objects.filter(username = username)

        if qs.exists():
            raise forms.ValidationError("Username is used")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs       = User.objects.filter(email = email)

        if qs.exists():
            raise forms.ValidationError("email is used")
        return email
    def clean(self):
        data            = self.cleaned_data
        password        = self.cleaned_data.get("password")
        password2       = self.cleaned_data.get("password2")

        if password != password2 :
            raise forms.ValidationError("password does not match")
        return data

class UserProfileForm(forms.ModelForm):
    email       =   forms.EmailField(widget=forms.EmailInput)
    password    =   forms.CharField(widget=forms.PasswordInput)
    password2   =   forms.CharField(widget=forms.PasswordInput,label="Confirm password")


    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs       = User.objects.filter(username = username)

        if qs.exists():
            raise forms.ValidationError("Username is used")
        return username
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs       = User.objects.filter(email = email)

        if qs.exists():
            raise forms.ValidationError("email is used")
        return email
    def clean(self):
        data            = self.cleaned_data
        password        = self.cleaned_data.get("password")
        password2       = self.cleaned_data.get("password2")

        if password != password2 :
            raise forms.ValidationError("password does not match")
        return data
    # def clean_avatar(self):
    #     avatar = self.cleaned_data['avatar']
    #     try:
    #         w, h = get_image_dimensions(avatar)
    #         print(w)
    #         print(h)


    #         # validate dimensions
    #         max_width = max_height = 100
    #         if w > max_width or h > max_height:
    #             raise forms.ValidationError(
    #                 u'Please use an image that is '
    #                  '%s x %s pixels or smaller.' % (max_width, max_height))
    #         print('check 0')

    #         # validate content type
    #         main, sub = avatar.content_type.split('/')
    #         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
    #             raise forms.ValidationError(u'Please use a JPEG, '
    #                 'GIF or PNG image.')
    #         print('check 1')
    #         #validate file size
    #         if len(avatar) > (20 * 1024):
    #             raise forms.ValidationError(
    #                 u'Avatar file size may not exceed 20k.')
    #         print('check 2')

    #     except :
    #         """
    #         Handles case when we are updating the user profile
    #         and do not supply a new avatar
    #         """
    #         # raise Http404("whaaaaaat inside")

    #     return avatar

class LikeForm(forms.Form):
    slug =forms.SlugField()
