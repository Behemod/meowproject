import json
import re

from venv import create

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from apps.notifications.utilities import create_notification

from .models import Meow, Like

@login_required
def api_add_meow(request):
    data = json.loads(request.body)
    body = data['body']

    meow = Meow.objects.create(body=body, created_by=request.user)

    results = re.findall("(^|[^@\w])@(\w{1,20})", body)

    for result in results:
        result = result[1]

        print(result)

        if User.objects.filter(username=result).exists() and result != request.user.ussername:
            create_notification(request, User.objects.get(username=result), 'mention')

    return JsonResponse({'success': True})

@login_required
def api_add_like(request):
    data = json.loads(request.body)
    meow_id = data['meow_id']

    if not Like.objects.filter(meow_id=meow_id).filter(created_by=request.user).exists():
        like = Like.objects.create(meow_id=meow_id, created_by=request.user)
        meow = Meow.objects.get(pk=meow_id)
        create_notification(request, meow.created_by, 'like')

    return JsonResponse({'success': True})