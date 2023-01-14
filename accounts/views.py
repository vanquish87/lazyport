from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# for flashing messages
from django.contrib import messages
from .models import Account


# Create your views here.
def profile(request):
    context = {}
    return render(request, 'account/profile.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        try:
            user = Account.objects.get(email=email)
        except:
            pass

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome Back!')
            return redirect(request.GET['next'] if 'next' in request.GET else 'profile')
        else:
            messages.warning(request, 'email or Password is incorrect')

    return render(request, 'account/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')
