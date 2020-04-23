from django.contrib import admin
from blog.models import Post, Comment
from accounts.models import UserProfile



# Register your models here.
class userProfileAdmin(admin.ModelAdmin):
    list_display    =   ['__str__']
    class Meta :
        model   =   UserProfile
        fields = '__all__'
        exclude = ['user']


class postAdmin(admin.ModelAdmin):
    list_display    =   ['__str__', 'slug']
    class Meta :
        model   =   Post

class commentAdmin(admin.ModelAdmin):
    list_display    =   ['__str__', 'slug']
    class Meta :
        model   =   Comment
# class likeAdmin(admin.ModelAdmin):
#     class Meta :
#         model   =   Likes
admin.site.register(UserProfile, userProfileAdmin)
admin.site.register(Post, postAdmin)
admin.site.register(Comment, commentAdmin)
# admin.site.register(Likes, likeAdmin)