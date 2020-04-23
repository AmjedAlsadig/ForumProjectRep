from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment 

class post_form(forms.ModelForm):   
    title = forms.CharField( label='')
    content = forms.CharField(widget=forms.Textarea, label='')
    image = forms.ImageField(label="")
    class Meta:
        model   =   Post
        fields = '__all__'
        exclude = ['auther','slug','like_count']
    def __init__(self, data=None, files=None, *args, **kwargs):
        super().__init__(data=data, files=files, *args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Post title'
        self.fields['content'].widget.attrs['placeholder'] = 'whats on your mind'
class comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['auther','post']
class LikeForm(forms.Form):
    slug =forms.SlugField()
