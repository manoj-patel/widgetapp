from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth import authenticate, login, logout
import os
import hmac
import hashlib
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'index.html')


def signUp(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     user = User.objects.create_user(username = username, password = password)
    #     user.save()
    #     user_hash = generate_hash(username)
    #     widget_token = os.getenv("WIDGET_TOKEN")

    #     return render(request, 'home.html', {"user_hash": user_hash, "widget_token": widget_token})

    # return render(request, 'signup.html')

def login_user(request):
   
    if request.user.is_authenticated:
        print(request.user.is_authenticated)
        username = request.user.username
        user_hash = generate_hash(username)
        widget_token = os.getenv("WIDGET_TOKEN")
        return render(request, 'home.html', {"user_hash": user_hash, "widget_token": widget_token})

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            user_hash = generate_hash(username)
            widget_token = os.getenv("WIDGET_TOKEN")
            
            return render(request, 'home.html', {"user_hash": user_hash, "widget_token": widget_token})

        else:
            messages.error(request, f'Invalid username or password')
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')


def generate_hash(unique_id):
    secret_key = os.getenv("SECRET_KEY")
    SECRET_KEY = secret_key.encode('ascii')
    UNIQUE_ID = unique_id.encode('ascii')
    hello_hash = hmac.new(SECRET_KEY, UNIQUE_ID, hashlib.sha256).hexdigest()
    return hello_hash


def logout_user(request):
    logout(request)
    return redirect('login')