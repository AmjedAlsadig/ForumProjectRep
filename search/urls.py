from django.conf.urls import url
from .views import   (  
    searchView
)

urlpatterns = [
    url(r'^',searchView,name='query'),
]