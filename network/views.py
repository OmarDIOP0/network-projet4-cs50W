import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_list_or_404,get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import User,Post,Follow


def index(request):
    posts = Post.objects.order_by('-created_at')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    posts_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{'posts_obj':posts_obj, 'posts': posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def new_post_view(request):
    if request.method == "POST":
        post_content = request.POST["content"]
        user = request.user
        if (post_content != ""):
            try:
                post = Post.objects.create(content=post_content, author=user)
                messages.success(request,"Post created successfully")
            except IntegrityError:
                messages.error(request,"Invalid post content")
        else:
            messages.error(request,"Post must not be empty")
            return HttpResponseRedirect(reverse("index"))       
    return HttpResponseRedirect(reverse("index"))
    

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    follower_count = Follow.objects.filter(follower = profile_user).count()
    following_count = Follow.objects.filter(following = profile_user).count()
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=profile_user).exists()
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    posts_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
            "profile_user":profile_user, 
            "posts":posts_obj, 
            "is_following":is_following,
            "follower_count":follower_count, 
            "following_count":following_count
              })

def follow(request, username):
    if request.user.is_authenticated:
        user_to_follow = get_object_or_404(User, username=username)
        Follow.objects.get_or_create(follower = request.user, following = user_to_follow)
    return HttpResponseRedirect(reverse("profile-view", args=[username]))

def unfollow(request, username):
    if request.user.is_authenticated:
        user_to_unfollow = get_object_or_404(User, username=username)
        Follow.objects.get(follower = request.user, following = user_to_unfollow).delete()
    return HttpResponseRedirect(reverse("profile-view", args=[username]))

@login_required
def following_view(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    posts_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {"posts_obj": posts_obj})


def edit_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            if request.user == post.author:
                data = json.loads(request.body)
                new_content = data.get('content', '')
                post.content = new_content
                post.save()
                return JsonResponse({'success': True, 'content': post.content})
            else:
                return JsonResponse({'success': False, 'error': 'Permission denied.'})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def toggle_like(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            user = request.user
            if user in post.likes.all():
                post.likes.remove(user)
                liked = False
            else:
                post.likes.add(user)
                liked = True
            post.save()
            return JsonResponse({'success': True, 'liked': liked, 'likes_count': post.likes.count()})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

