"""Forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.urls import path
from django.conf.urls import url
from .views import   (  List_view_function ,
                        detail_slug_view_function,
                        creat_post,
                        creat_comment,
                        people,
                        alter_friend,
                        follow,
                        Like,
                        Notifications_view
                    )


urlpatterns = [
   
    #account list view to display Posts
    # url(r'^posts/', List_view.as_view()),
    
    # url(r'^$', List_view_function, name='lsit_view'),
    
    # url(r'^posts-fbv/(?P<pk>\d+)/$', detail_view_function),
    
    url(r'^creatpost/$', creat_post, name='create_post'),
    url(r'^creatcomment/$', creat_comment, name='create_comment'),
    url(r'^(?P<slug>[\w]+)/$', detail_slug_view_function, name='detail'),
    url(r'^people',people,name='people'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', alter_friend, name='alter_friend'),   # path("<operation>/<pk>/", alter_friend, name="alter_friend")
    url(r'^follow/(?P<operation>.+)/(?P<pk>\d+)/$', follow, name='follow'),
    url(r'^like',Like,name='like'),
    url(r'^Notifications',Notifications_view,name='notification_name')
]
# url(r'^posts/$', List_view_function),
    
    # # url(r'^posts-fbv/(?P<pk>\d+)/$', detail_view_function),
    
    # url(r'^posts-fbv/(?P<slug>[\w]+)/$', detail_slug_view_function),
    # url(r'^posts/creatpost/$', creat_post),
    # url(r'^posts/creatcomment/$', creat_comment)