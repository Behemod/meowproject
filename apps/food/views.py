from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Meow

@login_required
def food(request):
    userids = [request.user.id]

    for meower in request.user.catprofile.follows.all():
        userids.append(meower.user.id)

    meows = Meow.objects.filter(created_by_id__in=userids)

    for meow in meows:
        likes = meow.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            meow.liked = True
        else:
            meow.liked = False

    return render(request, 'feed/food.html', {'meows': meows})

@login_required
def search(request):
    query = request.GET.get('query','')

    if len(query) > 0:
        meowers = User.objects.filter(username__icontains=query)
        meows = Meow.objects.filter(body__icontains=query)
    else:
        meowers = []
        meows = []

    context = {
        'query': query,
        'meowers': meowers,
        'meows': meows
    }

    return render(request, 'search.html', context)