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
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib import admin
from .views import home_page, profile_page, users_profile_page, search_page, login_page, register_page,logout_page
from ForumAccount.views import List_view_function, people
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', List_view_function, name='home'),
    url(r'^profile/', profile_page, name='profile'),
    # url(r'^search/', search_page, name='search'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login_page, name='login'),
    url(r'^logout/', logout_page, name='logout'),
    url(r'^register/', register_page, name='register'),
    url(r'^bootstrap/', TemplateView.as_view(template_name='bootstrap\example.html')),
    
    #account list view to display Posts
    url(r'^posts/', include('ForumAccount.urls', namespace='posts')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^people',people,name='people'),
    url(r'^users_profile/(?P<pk>\d+)/$', users_profile_page, name='users_profile'),
    
    
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)