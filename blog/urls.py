from django.conf.urls import url
from .views import   (
    detail_slug_view_function,
    Notifications_view,
    Like
)
urlpatterns = [
    url(r'^(?P<slug>[\w]+)/$', detail_slug_view_function, name='detail'),
    url(r'^Notifications',Notifications_view,name='notification_name'),
    url(r'^like',Like,name='like'),
]