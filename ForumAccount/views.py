import os
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import F,Q
from .models import Post, Comment , upload_file_to ,get_filename_and_ext, Friend, UserProfile, Likes
from .utils import unique_slug_generator
from .forms import post_form, comment_form,friends_form, LikeForm
from . import forms

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
            except Post.DoesNotExist :
                # post_query       =   None
                print('post query not found')
        #writeing post functionallity
        if request.user.is_authenticated() :        # @login_required
            if request.method == 'POST' :
                form        =  post_form(request.POST or None, request.FILES or None)
                context['form']= form
                if form.is_valid() :
                    instance    =  form.save(commit=False)
                    instance.auther = user
                    instance.save()        
            else :
                form = post_form()
        else :
            form = None
        context['form']= form
        return render(request, 'account/list_function.html', context)
    else :
        return redirect(reverse('login'))

def detail_slug_view_function(request,pk=None, slug=None, *args, **kwargs):
    # quering user
    try :
        user = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist :
        raise Http404("UserProfile.DoesNotExist")
    context ={
            'intiating' : 'intiating' 
            }  
    # quering post
    try: 
        instance        = get_object_or_404(Post, slug=slug)
    except Post.MultipleObjectsReturned:
        qs              = Post.objects.filter(slug=slug)
        post_instance        = qs.first()
        context['object'] = post_instance
        context['like_count'] =  post_instance.view_count()
    except:
        raise Http404("whaaaaaat")
    # quering comments
    try :
        Comment_instance    =   Comment.objects.filter(post=instance)
        print('checked')
        context['Comment']= Comment_instance
    except Comment.DoesNotExist :
       print('Comment_instance = None')
    context['object'] = post_instance
    context['like_count'] =  post_instance.view_count()
    # comment_form
    if request.user.is_authenticated() :        # @login_required
            if request.method == 'POST' :
                form        =  comment_form(request.POST or None, request.FILES or None)
            
                if form.is_valid() :
                    comment_instance    =  form.save(commit=False)
                    comment_instance.auther = user
                    comment_instance.post = instance 
                    comment_instance.save()      
                    print('checked')  
            else :
                form = comment_form()
            context['form'] = form
    else :
            form = None
    return render(request, 'account/detail_function.html', context)

@login_required(login_url="/login")
def creat_post(request):
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

@login_required(login_url="/login")
def creat_comment(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST' :
        form        =  comment_form(request.POST or None)
    
        if form.is_valid() :
            instance    =  form.save(commit=False)
            instance.auther =user
            instance.save()
            return redirect("../")
        
    else :
        form = comment_form()
    return render(request, "account/Create_post.html",{'form': form})

def people(request):
    try :
        people = UserProfile.objects.all()
    except UserProfile.DoesNotExist :
        raise Http404("UserProfile.DoesNotExist")
    except :
        raise Http404("except :")
    context = {
        "people":people,
    }
    return render(request, "people_page.html",context)
def follow(request, operation, pk):
    current_user = UserProfile.objects.get(user=request.user)
    to_be_followed    =   UserProfile.objects.get(pk=pk)
    if operation=='follow':
                Friend.follow(current_user,to_be_followed )
                print("follow list updated")
    if operation=='unfollow':
                Friend.un_follow(current_user, to_be_followed)
    return redirect("users_profile",pk=pk)

def alter_friend(request, operation, pk):
    current_user = UserProfile.objects.get(user=request.user)
    new_friend    =   UserProfile.objects.get(pk=pk)
    if operation=='add':
        Friend.add_friend(current_user, new_friend)
        print("Friend list updated")
    if operation=='remove':
        Friend.remove_friend(current_user, new_friend)
    return redirect("users_profile",pk=pk)
def Like_post(user,post_id):
    new_like , created = Likes.objects.get_or_create(post=post_id,likes_list=user)
    if not created :
        Likes.objects.filter(likes_list=user,post=post_id).delete()
        post_id.like_count = post_id.view_count()
        print('like removed')
    else:
        post_id.like_count = post_id.view_count()
        print(post_id.like_count)
        print('liked sucssefuly')
@login_required
def Like(request):
    user = UserProfile.objects.get(user=request.user)
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
            # like_instane = Likes.likes_list.through.objects.get(userprofile=user)
            print('Like_instance founded')
        except Post.DoesNotExist :
            like_instane = None
            like_instane_bool = True
        except :
            like_instane = None
            like_instane_bool = True
        print('calling like_post')
        try :
            like_state_query = Likes.likes_list.through.objects.get(userprofile=user)
        except  :
            like_state_query = None
        try :
            like_obj = like_state_query.filter(post=post)
        except  :
            like_obj  = None
        if like_state_query is None:
            Likes.add_like(post,user)
            print("Like")
        else:
            Likes.remove_like(post,user)
            print("DisLike")
        print('after like')
    return redirect('home')