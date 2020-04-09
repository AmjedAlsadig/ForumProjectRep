from django.contrib.auth import authenticate, login, get_user_model, logout 
from django.http import HttpResponse, Http404
from django.shortcuts import render ,redirect
from django.urls import reverse
from .forms import  loginForm, registerForm
from ForumAccount.models import Friend, Post, UserProfile
from ForumAccount.forms import UserProfileForm

def home_page(request):
    context = {
        "title"         :   "Home Page",
        "description"   :   "Welcome to the home page"
    }
    if request.user.is_authenticated() :
        context ["premium"] = "hyee this is the premium content"
    return render(request, "home_page.html", context)

def profile_page(request):
    if request.user  :
        print("checked")
        context = {
             "title"         :   "Profile",
            "description"   :   "Welcome to the Profile page",
        }
        try :
            user    =   UserProfile.objects.get(user=request.user)
            avatar        =user.avatar.url
            context["avatar"] = avatar
            context['username'] = user.__str__
            context['user'] = user
        except :
            raise Http404("Not working , check back later")
        print("checked")
        # if user.is_authenticated :
        if user:
            try:
                new_qs       =   Friend.objects.get(current_user=user)
                friend_list  = new_qs.friend_list.all()
                context["friend_list"] = friend_list
            except Friend.DoesNotExist :
                print("Friend.DoesNotExist")
            except :
                print("Friend.DoesNotExist")
            try:
                posts        = Post.objects.all().filter(auther=user).order_by('-time')
                context["posts"] = posts
            except Post.DoesNotExist :
                print("Posts.DoesNotExist")
    return render(request, "Profile.html", context)

def users_profile_page(request, pk):
    context = {
        "title"         :   "Profile",
        "description"   :   "Welcome to the Profile page",
        "pk"            :   pk
    }
    try :
        user    =   UserProfile.objects.get(pk=pk)
        print(user)
        avatar =user.avatar.url
        print("found the pic")
        context["avatar"] = avatar
        context['username'] = user.__str__
        context['user'] = user
    except :
        raise Http404("user not found")
    try :
        new_qs       =   Friend.objects.get(current_user=user)
        friend_list  = new_qs.friend_list.all()
        context["friend_list"] = friend_list
    except Friend.DoesNotExist :
        new_qs = None
        print('Friend.DoesNotExist')
    if new_qs is not None : 
        try :
            request_user = request.user
            friendship_state_query = Friend.friend_list.through.objects.get(userprofile=user)
            print('friendship_state_query found')
            friendship_state = "remove"
            context['remove'] = friendship_state
        except Friend.DoesNotExist :
            friendship_state = "add"
            context['add'] = friendship_state
        except  :
            friendship_state = "add"
            context['add'] = friendship_state
    else:
        friendship_state = "add"
        context['add'] = friendship_state
    try :
        posts        = Post.objects.all().filter(auther=user).order_by('-time')
        context["posts"] = posts
    except Post.DoesNotExist :
       print('Post.DoesNotExist')
    return render(request, "Profile.html", context)

def search_page(request):
    context = {
        "title"         :   "Serach Page",
        "description"   :   "Welcome to the Search page"
    }
    return render(request, "home_page.html", context)

def login_page(request):
    form    =   loginForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username    = form.cleaned_data.get("username")
        password    = form.cleaned_data.get("password")
        user        = authenticate(request ,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else :
            print("error")
    context = {
            "form"      :   form ,
            # "url"       :   request.url 
            
        }
    return render(request, "auth/login_page.html",context)
def logout_page(request):
    logout(request)
    return redirect(reverse('login'))
User = get_user_model()

def register_page(request):
    # form  = registerForm(request.POST or None)
    form = UserProfileForm(request.POST or None, request.FILES or None)
    context = {
            "form"  :   form
        }
    if form.is_valid():
        print('check')
        instance = form.save(commit=False)
        print(form.cleaned_data)
        username    =   form.cleaned_data.get("username")
        password    =   form.cleaned_data.get("password")
        email       =   form.cleaned_data.get("email")
        new_user    =   User.objects.create_user(username, email, password)
        instance.user = new_user
        instance.save()
        print(new_user)
        return redirect("/")
    else :
        form = UserProfileForm()
    return render(request, "auth/register_page.html", context)