import os
from django.shortcuts import render, get_object_or_404, Http404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import F,Q
from django.utils.timezone import now
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.auth import authenticate, login, get_user_model, logout 
#COSTUM IMPORTS 
from Forum.forms import EditProfileForm
from .models import Friend, UserProfile,FriendRequest
from .forms import  loginForm, registerForm, UserProfileForm
from blog.models import  Post,Notifications

def create_notify(sender,post,action_type,reciever):
    print('create_notify')
    # try :
    print('friend found')
    notif = Notifications.add_nofi(sender,post,action_type,reciever)
    print('reciver added')
    print(action_type)
    print('done')
    # except :
        # print('Notification not created')  
        # print(action_type)
def notify_context(user,context):
    print('notify_context')
    #querying  Notifications
    try :
        print(user)
        print('check 0')
        noti = Notifications.objects.filter(receivers=user)
        noti_no_qs = noti.filter(read_at=None)
        print(noti_no_qs.count())
        context['Notifications'] = noti
        context["notification_no"] = noti_no_qs.count()
        context["user"] = user
        print('check 1')
        print("check 2")
    except :
        print('except :')
        print('noti not found')
def friend_requests_context(user,context):
    print('friend_requests_context')
    #querying  FriendRequest
    try :
        print(user)
        print('check 0')
        friend_request = FriendRequest.objects.filter(Q(receiver=user)&Q(delete=False))
        print('check 0')
        context['friend_request'] = friend_request
        req_no = friend_request.count()
        context["req_no"] = req_no
        print(req_no)
        print('check 0')    
    except  :
        print('except :')
        print('req not found')   
def people(request):
    # quering user
    try :
        user = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist :
        raise Http404("UserProfile.DoesNotExist")
    except :
        return redirect('home')
    try :
        people = UserProfile.objects.all()
    except UserProfile.DoesNotExist :
        raise Http404("UserProfile.DoesNotExist")
    except :
        raise Http404("except :")
    context = {
        "people":people,
    }
    # querying notifications
    notify_context(user,context)
    friend_requests_context(user,context)
    return render(request, "people_page.html",context)
def follow(request, operation, pk):
    current_user = UserProfile.objects.get(user=request.user)
    to_be_followed    =   UserProfile.objects.get(pk=pk)
    if operation=='follow':
                Friend.follow(current_user,to_be_followed )
                print("follow list updated")
    if operation=='unfollow':
                Friend.un_follow(current_user, to_be_followed)
    return redirect("accounts:users_profile",pk=pk)
def friend_request(request,pk):
    current_user = UserProfile.objects.get(user=request.user)
    new_friend = UserProfile.objects.get(pk=pk)
    try :
        friend_request_qs,created = FriendRequest.objects.get_or_create(
            sender=current_user,
            receiver=new_friend,
            requested=True,
            delete = False,
            read_at = None,
            accepted= False
        )
        print(' friend_request sent')
    except :
        print('exception :(')
    return redirect("accounts:users_profile",pk=pk)
def accept_request(request,pk):
    print("accept")
    current_user = UserProfile.objects.get(user=request.user)
    new_friend = UserProfile.objects.get(pk=pk)
    try :
        friend_request_qs,created = FriendRequest.objects.get_or_create(sender=new_friend,receiver=current_user,requested=True)
        friend_request_qs.accepted = True
        friend_request_qs.delete = True
        friend_request_qs.save()
        print("accept check 1")
        try :
            qs=FriendRequest.objects.get(Q(sender=new_friend)&Q(receiver=current_user))
            print("accept check 2")
            bool = True
        except FriendRequest.DoesNotExist :
            bool = null
        except :
            print("exception")
            bool = null
        print("accept check 3")
        print(bool)
        if (bool == True) and (qs.accepted == True) :
            print("accept check 4")
            Friend.add_friend(current_user, new_friend)
            qs.read_at = now()
            qs.save()
            qs.delete()
            print('qs.delete()')
            qs.save()
            print(qs.read_at)
            print("Friend list updated")
    except :
        print('exception :(')
    return redirect("accounts:users_profile",pk=pk)
def ignore_request(request,pk):
    print('ignore :')
    current_user = UserProfile.objects.get(user=request.user)
    new_friend = UserProfile.objects.get(pk=pk)
    # try :
    friend_request_qs,created = FriendRequest.objects.get_or_create(sender=current_user,receiver=new_friend,requested=True)
    print('check 1')
    friend_request_qs.read_at = now()
    print('check 2')
    print("Friend list updated")
    friend_request_qs.accepted = False
    print('check 3')
    friend_request_qs.delete = True
    print('check 4')
    friend_request_qs.save()
    print('check 5')
    friend_request_qs.delete()
    print('check 6')
    friend_request_qs.save()
    print('check 7')
        # try :
        #     qs=FriendRequest.objects.get(Q(sender=current_user)&Q(receiver=new_friend))
        #     bool = True
        # except FriendRequest.DoesNotExist :
        #     bool = False
        # except :
        #     print("exception")
        # if (bool == True):
        #     qs.read_at = now()
        #     print("Friend list updated")
    # except :
    #     print('exception :(')
    print('end of ignore')
    return redirect("accounts:users_profile",pk=pk)
def remove_friend(request,pk):
    current_user = UserProfile.objects.get(user=request.user)
    new_friend = UserProfile.objects.get(pk=pk)
    Friend.remove_friend(current_user, new_friend)
    return redirect("accounts:users_profile",pk=pk)
def Friend_request_view(request):
    try :
        active_user = UserProfile.objects.get(user=request.user)
    except :
        return redirect('home')
    context = {
        'initilze' : 'initilze'
    }
    
    # try :
    notify_context(active_user,context)
    friend_requests_context(active_user,context)
    # except :
        # raise Http404("Notifications page eror")
    return render(request,'friend_requests.html',context)

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
            context['edit'] = 'edit'
        except :
            return redirect('home')
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
            #querying notifications
            notify_context(user,context)
            friend_requests_context(user,context)
    return render(request, "Profile.html", context)

def users_profile_page(request, pk):
    context = {
        "title"         :   "Profile",
        "description"   :   "Welcome to the Profile page",
        "pk"            :   pk
    }
    active_user = UserProfile.objects.get(user=request.user)
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
    if user==UserProfile.objects.get(user=request.user):
        return redirect("accounts:profile")
    else :

        try :
            new_qs       =   Friend.objects.get(current_user=user)
            friend_list  = new_qs.friend_list.all()
            context["friend_list"] = friend_list
        except Friend.DoesNotExist :
            new_qs = None
            print('Friend.DoesNotExist')
        if new_qs is not None : 
            try :
                # friendship_state_query = Friend.friend_list.through.objects.get(userprofile=user)
                # friendship_state_query = new_qs.friend_list.through.objects.get(userprofile=active_user)
                friendship_state_query = Friend.objects.get(Q(current_user=active_user)&Q(friend_list=user))
                print('friendship_state_query found')
                friendship_state = "remove"
                context['remove'] = friendship_state
            except Friend.DoesNotExist :
                friendship_state = "add"
                context['add'] = friendship_state
            except  :
                friendship_state = "add"
                context['add'] = friendship_state
            try :
                following_state_query = Friend.objects.get(Q(current_user=active_user)&Q(following=user))
                # following_state_query = new_qs.following.through.objects.get(userprofile=active_user)
                print('following_state_query found')
                follow_state = "unfollow"
                context['unfollow'] = follow_state
            except Friend.DoesNotExist :
                follow_state = "follow"
                context['follow'] = follow_state
            except  :
                follow_state = "follow"
                context['follow'] = follow_state
        else:
            follow_state = "follow"
            context['follow'] = follow_state
            friendship_state = "add"
            context['add'] = friendship_state
        try :
            posts        = Post.objects.all().filter(auther=user).order_by('-time')
            context["posts"] = posts
        except Post.DoesNotExist :
            print('Post.DoesNotExist')
        notify_context(active_user,context)
        friend_requests_context(active_user,context)
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
    return redirect(reverse('accounts:login'))
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
@login_required(login_url="/login")
def edit_profile(request):
    user=UserProfile.objects.get(user=request.user)
    context = {
        'init' : 'init'
    }
    if request.method == 'POST' :
        form = EditProfileForm(request.POST,instance=user.user)
        if form.is_valid() :
            form.save()
            return redirect('profile')
    else :
        form = EditProfileForm(instance=user.user)
        context['form'] = form
        return render(request,'EditProfilePage.html',context)
@login_required(login_url="/login")
def change_password(request):
    user=UserProfile.objects.get(user=request.user)
    context = {
        'init' : 'init'
    }
    if request.method == 'POST' :
        form = PasswordChangeForm(request.POST,instance=user.user)
        if form.is_valid() :
            form.save()
            return redirect('profile')
    else :
        form = PasswordChangeForm(instance=user.user)
        context['form'] = form
        return render(request,'change_password.html',context)
