from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Secretary
from django.contrib import messages
import requests, json


def redirecting(request):
    return redirect('home')

def home(request):
    try:
        if request.session['loggedIn']:
            username = request.session['username']
            return render(request, 'home/camera.html', {'username': username, 'path':'/static/vids/VID-20250513-WA0026.mp4'})
    except:
        return redirect('login')
    return redirect('login')

def logout(request):
    request.session['loggedIn'] = False
    request.session['username'] = 'No User!'
    return redirect('login')

def login(request):
    try:
        if request.session['loggedIn']:
            return redirect('home')
    except:
        pass
    if request.method == "POST":
        POST_username = request.POST.get('username')
        filledName:bool = bool(len(POST_username))
        POST_password = request.POST.get('password')
        filledPass:bool = bool(len(POST_password))
        nextPage = request.POST.get('next')

        if not filledName or not filledPass:
            messages.error(request, 'All fields must be filled!')
            return redirect('login')

        sec = Secretary.objects.filter(username=POST_username, password=POST_password)
        if len(sec) != 0:
            request.session['loggedIn'] = True
            request.session['username'] = POST_username
            return redirect('home')

        messages.error(request, 'Credentials are invalid!')
        return redirect('login')
        
    return render(request, "accounts/login.html")

def dashboard(request):
    try:
        if request.session['loggedIn']:
            pass
        else:
            return redirect('login')
    except:
        return redirect('login')
    username = request.session['username']
    res = requests.get(f'http://{request.get_host()}/detector/api/dashboard/today/')
    res.raise_for_status()
    data = res.json()
    return render(request, 'home/dashboard.html', {'username': username, 'dash': data})

def log(request):
    try:
        if request.session['loggedIn']:
            pass
        else:
            return redirect('login')
    except:
        return redirect('login')
    username = request.session['username']
    res = requests.get(f'http://{request.get_host()}/detector/api/violations/all/')
    res.raise_for_status()
    data = res.json()
    return render(request, 'home/log.html', {'username': username, 'logs': data})

def getImage(request, imgID):
    try:
        with open(f'images/alerts/violator{imgID}.png', 'rb') as imgFile:
            return HttpResponse(imgFile.read(), content_type='image/png')
    except FileNotFoundError:
        return HttpResponse("Image not found", status=404)