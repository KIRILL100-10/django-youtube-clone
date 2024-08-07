from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserChangeForm
from .forms import RegisterForm, LoginForm, UserProfileForm, VideoForm, CommentForm
from .models import Like, Subscription, Video, Comment
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    videos = Video.objects.all()
    return render(request, 'main/home.html', {'videos': videos})

def search(request):
    query = request.GET.get('q')
    if query:
        videos = Video.objects.filter(title__icontains=query)
    else:
        videos = Video.objects.all()
    return render(request, 'main/search_results.html', {'videos': videos, 'query': query})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('home')
    return render(request, 'main/logout.html')

@login_required
def profile(request):
    videos = Video.objects.filter(author=request.user)
    return render(request, 'main/profile.html', {'videos': videos})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'main/profile_edit.html', {'form': form})


@login_required
def profile_delete_confirm(request):
    return render(request, 'main/profile_delete_confirm.html')


@login_required
def profile_delete(request):
    request.user.delete()
    messages.success(request, 'Profile deleted successfully.')
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    return redirect('video_detail', video_id=comment.video.id)

@login_required
def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user
            video.save()
            return redirect('profile')
    else:
        form = VideoForm()
    return render(request, 'main/add_video.html', {'form': form})

@login_required
def video_edit(request, video_id):
    video = get_object_or_404(Video, id=video_id, author=request.user)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = VideoForm(instance=video)
    return render(request, 'main/video_edit.html', {'form': form})

@login_required
def video_delete(request, video_id):
    video = get_object_or_404(Video, id=video_id, author=request.user)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully.')
        return redirect('profile')
    return render(request, 'main/video_delete.html', {'video': video})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile_edit.html', {'form': form})


@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    like, created = Like.objects.get_or_create(user=request.user, video=video)
    if not created:
        like.delete()
    return JsonResponse({'liked': created, 'total_likes': video.like_set.count()})

@login_required
def subscribe_channel(request, channel_id):
    channel = get_object_or_404(User, id=channel_id)
    subscription, created = Subscription.objects.get_or_create(user=request.user, channel=channel)
    if not created:
        subscription.delete()
    return JsonResponse({'subscribed': created, 'total_subscribers': channel.subscribers.count()})

@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments = video.comment_set.all()
    is_liked = video.like_set.filter(user=request.user).exists()
    is_subscribed = request.user.subscribed_to.filter(channel=video.author).exists()
    return render(request, 'main/video_detail.html', {
        'video': video,
        'comments': comments,
        'is_liked': is_liked,
        'is_subscribed': is_subscribed,
        'total_likes': video.like_set.count(),
        'total_subscribers': video.author.subscribers.count()
    })
    
@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('video_detail', video_id=video_id)
    else:
        form = CommentForm()
    return render(request, 'main/add_comment.html', {'form': form, 'video': video})


@login_required
def edit_comment(request, video_id, comment_id):
    video = get_object_or_404(Video, id=video_id)
    comment = get_object_or_404(Comment, id=comment_id, video=video, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('video_detail', video_id=video_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'main/edit_comment.html', {'form': form, 'video': video})