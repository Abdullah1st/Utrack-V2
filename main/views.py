from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Secretary
from django.contrib import messages
import requests, json, os


def redirecting(request):
    return redirect('home')

@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username
    return render(request, 'home/camera.html', {'username': username, 'path':'/static/vids/'})

def logout(request):
    auth_logout(request)
    return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        POST_username = request.POST.get('username')
        POST_password = request.POST.get('password')
        if not POST_username or not POST_password:
            messages.error(request, 'All fields must be filled!')
            return render(request, "accounts/login.html")

        sec = authenticate(request, username=POST_username, password=POST_password)
        if sec is not None:
            login(request, sec)

        messages.error(request, 'Credentials are invalid!')
        
    return render(request, "accounts/login.html")

@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username
    res = requests.get(f'http://{request.get_host()}/detector/api/dashboard/today/')
    res.raise_for_status()
    data = res.json()
    return render(request, 'home/dashboard.html', {'username': username, 'dash': data})

@login_required
def log(request):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username
    res = requests.get(f'http://{request.get_host()}/detector/api/violations/all/')
    res.raise_for_status()
    data = res.json()
    return render(request, 'home/log.html', {'username': username, 'logs': data})

def getImage(request, imgID):
    try:
        with open(f'images/alerts/{imgID}', 'rb') as imgFile:
            return HttpResponse(imgFile.read(), content_type='image/jpg')
    except FileNotFoundError:
        return HttpResponse("Image not found", status=404)