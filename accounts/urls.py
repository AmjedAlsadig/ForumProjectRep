from django.conf.urls import url

from .views import   (
    people, 
    follow,
    accept_request,
    remove_friend,
    friend_request,
    ignore_request,
    Friend_request_view,
    profile_page, 
    users_profile_page, 
    login_page, 
    register_page,
    logout_page,
    edit_profile,
    change_password
)
urlpatterns = [
    url(r'^profile/$', profile_page, name='profile'),
    url(r'^login/', login_page, name='login'),
    url(r'^logout/', logout_page, name='logout'),
    url(r'^register/', register_page, name='register'),
    url(r'^Profile/edit$', edit_profile, name='edit'),
    url(r'^Profile/edit/password', change_password, name='changePassword'),
    url(r'^users_profile/(?P<pk>\d+)/$', users_profile_page, name='users_profile'),
    url(r'^people',people,name='people'),
    url(r'^follow/(?P<operation>.+)/(?P<pk>\d+)/$', follow, name='follow'),
    url(r'^Friend_request_view',Friend_request_view,name='Friend_request_view'),
    url(r'^friend_request/(?P<pk>\d+)/$', friend_request, name='friend_request'),#send request
    url(r'^accept_request/(?P<pk>\d+)/$', accept_request, name='accept_request'),#accepte request
    url(r'^ignore_request/(?P<pk>\d+)/$', ignore_request, name='ignore_request'),#ignore request
    url(r'^remove_friend/(?P<pk>\d+)/$', remove_friend, name='remove_friend'),#remove friend
]
