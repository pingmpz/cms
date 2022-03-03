from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from dateutil import parser
# Authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def first_page(request):
    context = {
    }
    return render(request, 'first_page.html', context)

def login_page(request):
    context = {
    }
    return render(request, 'login_page.html', context)

def validate_login(request):
    canLogIn = False
    invalidText = ""
    invalidList = []
    username = request.GET['username']
    password = request.GET['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        canLogIn = True
    else:
        invalidText = "Username or Password is not correct."
        invalidList = ["username","password"]
    data = {
        'canLogIn': canLogIn,
        'invalidText': invalidText,
        'invalidList': invalidList,
    }
    return JsonResponse(data)

def login_action(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/index/MY')
    return redirect('/')

@login_required(login_url='/')
def logout_action(request):
    logout(request)
    return redirect('/')

def new_request(request):
    context = {
    }
    return render(request, 'new_request.html', context)

@login_required(login_url='/')
def index(request, freq):
    context = {
        'freq': freq,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'index.html', context)

@login_required(login_url='/')
def request_page(request, request_no):
    requestIsExist = False
    requestIsExist = True
    status = 'None'
    if request_no == 'CMS000001':
        status = 'On Progress'
    elif request_no == 'CMS000002':
        status = 'On Hold'
    elif request_no == 'CMS000003':
        status = 'Pending'
    elif request_no == 'CMS000004':
        status = 'Rejected'
    elif request_no == 'CMS000005':
        status = 'Complete'
    elif request_no == 'CMS000006':
        status = 'Canceled'
    context = {
        'request_no': request_no,
        'requestIsExist': requestIsExist,
        'status': status,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_page.html', context)

@login_required(login_url='/')
def pending_request(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'pending_request.html', context)

@login_required(login_url='/')
def history_request(request, freq, fstatus, fstartdate, fstopdate):
    if fstartdate == "NOW":
        fstartdate = datetime.today().strftime('%Y-%m-%d')
    if fstopdate == "NOW":
        fstopdate = datetime.today().strftime('%Y-%m-%d')
    context = {
        'freq': freq,
        'fstatus': fstatus,
        'fstartdate': fstartdate,
        'fstopdate': fstopdate,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'history_request.html', context)

def new_pv_request(request):
    context = {
    }
    return render(request, 'new_pv_request.html', context)

@login_required(login_url='/')
def emp_master(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'emp_master.html', context)

@login_required(login_url='/')
def mc_master(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'mc_master.html', context)

@login_required(login_url='/')
def vendor_master(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'vendor_master.html', context)

@login_required(login_url='/')
def cat_master(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'cat_master.html', context)

def all_page_data(request):
    my_request_counts = 2
    pending_request_counts = 1
    context = {
        'my_request_counts': my_request_counts,
        'pending_request_counts': pending_request_counts,
    }
    return context
