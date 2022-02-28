from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from dateutil import parser
# Authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def login_page(request):
    context = {
    }
    return render(request, 'login_page.html', context)

def login_action(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/index/')
    return redirect('/')

@login_required(login_url='/')
def logout_action(request):
    logout(request)
    return redirect('/')

def index(request):
    context = {
    }
    return render(request, 'index.html', context)

def new_request(request):
    context = {
    }
    return render(request, 'new_request.html', context)
