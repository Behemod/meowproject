from webbrowser import get
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from pkg_resources import cleanup_resources

from apps.notifications.utilities import create_notification

from .forms import CatProfileForm, SignUpForm
from .models import CatProfile

def catprofile(request, username):
    user = get_object_or_404(User, username=username)
    meows = user.meows.all()

    for meow in meows:
        likes = meow.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            meow.liked = True
        else:
            meow.liked = False

    context = {
        'user': user,
        'meows': meows
    }

    return render(request, 'catprofile.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        catprofileform = CatProfileForm(request.POST, request.FILES)

        if form.is_valid() and catprofileform.is_valid():
            user = form.save()

            catprofile = catprofileform.save(commit=False)
            catprofile.user = user
            catprofile.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
        catprofileform = CatProfileForm()
    
    return render(request, 'signup.html', {'form': form, 'catprofileform': catprofileform})

@login_required
def follow_meower(request, username):
    user = get_object_or_404(User, username=username)

    request.user.catprofile.follows.add(user.catprofile)

    create_notification(request, user, 'follower')

    return redirect('catprofile', username=username)

@login_required
def unfollow_meower(request, username):
    user = get_object_or_404(User, username=username)

    request.user.catprofile.follows.remove(user.catprofile)

    return redirect('catprofile', username=username)

def followers(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'followers.html', {'user': user})

def follows(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'follows.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CatProfileForm(request.POST, request.FILES, instance=request.user.catprofile)

        if form.is_valid():
            form.save()

            return redirect('catprofile', username=request.user.username)
    else:
        form = CatProfileForm(instance=request.user.catprofile)

    context = {
        'user': request.user,
        'form': form
    }

    return render(request, 'edit_profile.html', context)