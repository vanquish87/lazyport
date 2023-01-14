from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='login')
def index(request):
    settings.SESSION_COOKIE_AGE = 600
    context = {}
    return render(request, 'index/index.html', context)
