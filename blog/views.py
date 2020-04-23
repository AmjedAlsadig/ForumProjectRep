import os
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import F,Q
from django.utils.timezone import now
#COSTUM IMPORT
from .models import Post, Comment, Notifications,Likes
from accounts.models import Friend, UserProfile ,FriendRequest
# from accounts.views import friend_requests_context
from .forms import post_form, comment_form


# Create your views here.
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
def List_view_function(request):
    if request.user.is_authenticated() :       # @login_required
        # quering user
        try :
            user = UserProfile.objects.get(user=request.user)
            print('user founded')
        except UserProfile.DoesNotExist :
            raise Http404('Damn it :(')
        # creating context
        context ={
            'intiating' : 'intiating' 
            }             
        #quering friends
        try :
            new_qs       =   Friend.objects.get(current_user=user)
            print('friend query')
            friend_list_context = new_qs.friend_list.all()
            print('friend query found')
            context['friend_list'] = friend_list_context 
        except Friend.DoesNotExist :
            # new_qs = None
            # friend_list  = None
            # friend_list_context = None
            print('friend query not found')
        except :
            # new_qs = None
            # friend_list  = None
            # friend_list_context = None
            print("new_qs       =   Friend.objects.get(current_user=user) not found")
        #quering post
        try :
            following = Friend.objects.get(current_user=user)
        except Friend.DoesNotExist:
            print("Friend.DoesNotExist")
            following = None
        except :
            print("except :")
            following = None
        if following is not None:
            # querying for self and folllowing posts
            try :
                post_query = Post.objects.filter(Q(auther__in =following.following.all())|Q(auther=user)).order_by('-time')
                print('post query found')
                context['post_list'] = post_query
                print('context + post_list')
            except Post.DoesNotExist :
                # post_query       =   None
                print('post query not found')
            
        else :
            try :
                post_query        =   Post.objects.get(auther=user).order_by('-time')
                print('post query found')
                context['post_list'] = post_query
                print('context + post_list')
                try :
                    noti = Notifications.receivers.through.objects.get(userprofile=user)
                    noti_post = noti.post
                    print(noti_post.title)
                except :
                    print('except :')
                    print('noti not found')
            except Post.DoesNotExist :
                # post_query       =   None
                print('post query not found')
        #querying  Notifications
        notify_context(user,context)
        friend_requests_context(user,context)
        # #writeing post functionallity
        if request.user.is_authenticated() :        # @login_required
            if request.method == 'POST' :
                form        =  post_form(request.POST or None, request.FILES or None)
                context['form']= form
                if form.is_valid() :
                    instance    =  form.save(commit=False)
                    instance.auther = user
                    instance.save()
                    sender = user
                    # creating notification
                    action_type = 'posted'
                    create_notify(sender,instance,action_type,friend_list_context)
            else :
                form = post_form()
        else :
            form = None
        context['form']= form
        return render(request, 'account/list_function.html', context)
    else :
        return redirect(reverse('accounts:login'))
def detail_slug_view_function(request,pk=None, slug=None, *args, **kwargs):
    # quering user
    try :
        user = UserProfile.objects.get(user=request.user)
    except :
        return redirect('home')
    context ={
            'intiating' : 'intiating' 
            }  
    # quering post
    try: 
        instance = get_object_or_404(Post, slug=slug)
        context['object'] = instance
        context['like_count'] = instance.Likes_count()
        context['comment_count'] = instance.comments_count()
    except Post.MultipleObjectsReturned:
        qs = Post.objects.filter(slug=slug)
        post_instance = qs.first()
        context['object'] = post_instance
        context['like_count'] = post_instance.Likes_count()
        context['comment_count'] = post_instance.comments_count()
    try :
        Comment_instance = Comment.objects.filter(post=instance)
        print('checked')
        context['Comment']= Comment_instance
    except Comment.DoesNotExist :
       print('Comment_instance = None')
    #quering friends
    try :
        new_qs = Friend.objects.get(current_user=user)
        print('friend query')
        friend_list_context = new_qs.friend_list.all()
        print('friend query found')
    except Friend.DoesNotExist :
        print('friend query not found')  
    try :
        qs_notify = Notifications.objects.filter(Q(post=instance)&Q(receivers=user)&Q(read_at=None))
    except :
        print('not found qs_notify = Notifications.objects.get(post=instance)')
    # qs_notify.read_at = datetime
    # qs_notify.save()
    for i in qs_notify :
        i.read_at = now()
        i.save()
        print(i.read_at)
    # comment_form
    if request.user.is_authenticated() :        # @login_required
            if request.method == 'POST' :
                form = comment_form(request.POST or None, request.FILES or None)
                if form.is_valid() :
                    comment_instance = form.save(commit=False)
                    comment_instance.auther = user
                    comment_instance.post = instance 
                    comment_instance.save()      
                    print('checked')
                    # creating notification
                    action_type = 'commented'
                    create_notify(user,instance,action_type,friend_list_context)
            else :
                form = comment_form()
            context['form'] = form
    else :
            form = None
    #querying  Notifications
    notify_context(user,context)
    friend_requests_context(user,context)
    return render(request, 'account/detail_function.html', context)


    if request.method == 'POST' :
        form        =  post_form(request.POST or None, request.FILES or None)
    
        if form.is_valid() :
            instance    =  form.save(commit=False)
            instance.auther = request.user
            # instance.image = form.image
            instance.save()
            return redirect("../")
        
    else :
        form = post_form()
    # context         =   { 
    #         "form"  :   form 
    #     } 
    return render(request, "account/Create_post.html",{'form': form})
@login_required
def Like(request):
    try :
       user = UserProfile.objects.get(user=request.user)
    except :
        return redirect('home')
    print('user found')
    if request.POST :
        slug = request.POST.get('like_post_slug')
        print(slug)
        # quering post
        try :
            post = Post.objects.get(slug=slug)
            print('post founded')
        except Post.DoesNotExist :
            post = None
        like_instane_bool = False
        try :
            like_instane = Likes.objects.get(post=post)
            print('Like_instance founded')
        except Post.DoesNotExist :
            like_instane = None
            like_instane_bool = True
        except :
            like_instane = None
            like_instane_bool = True
        print('calling like_post')
        if like_instane  is not None :
            try :
                # like_state_query = like_instane.likes_list.through.objects.get(userprofile=user)
                like_state_query = Likes.objects.get(Q(post=post)&Q(likes_list=user))
                print("fdhgdhet")
            except :
                like_state_query = None
                print("aaaa")
        else  :
            like_state_query = None
        # querying friends
        try :
            new_qs       =   Friend.objects.get(current_user=user)
            print('friend query')
            friend_list_context = new_qs.friend_list.all()
            print('friend query found')
        except Friend.DoesNotExist :
            print('friend query not found')
        if like_state_query is None:
            Likes.add_like(post,user)
            # creating notification
            action_type = 'Liked'
            create_notify(user,post,action_type,friend_list_context)
            print("Like")
        else:
            Likes.remove_like(post,user)
            print("DisLike")
        print('after like')
    return redirect('home')
def Notifications_view(request):
    context = {
        'initilze' : 'initilze'
    }
    try :
        active_user = UserProfile.objects.get(user=request.user)
    except :
        return redirect('home')
    try :
        notify_context(active_user,context)
        friend_requests_context(active_user,context)
    except :
        raise Http404("Notifications page eror")
    return render(request,'Notifications.html',context)

    context = {
        'initilze' : 'initilze'
    }
    try :
        active_user = UserProfile.objects.get(user=request.user)
    except :
        raise Http404('user not found >>> Notifications_view')
    # try :
    notify_context(active_user,context)
    friend_requests_context(active_user,context)
    # except :
        # raise Http404("Notifications page eror")
    return render(request,'friend_requests.html',context)