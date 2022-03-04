from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from dateutil import parser
# Authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Employee

################################# Authenticate #################################
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
    username = request.GET['username']
    password = request.GET['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        canLogIn = True
    data = {
        'canLogIn': canLogIn,
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

##################################### Page #####################################

def new_request(request):
    context = {
    }
    return render(request, 'new_request.html', context)

def new_pv_request(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_pv_request.html', context)

@login_required(login_url='/')
def request_page(request, request_no):
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
    else:
        requestIsExist = False
    context = {
        'request_no': request_no,
        'requestIsExist': requestIsExist,
        'status': status,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_page.html', context)

#------------------------------------ Main ------------------------------------#

def all_page_data(request):
    my_request_counts = 2
    pending_request_counts = 1
    context = {
        'my_request_counts': my_request_counts,
        'pending_request_counts': pending_request_counts,
    }
    return context

@login_required(login_url='/')
def index(request, freq):
    context = {
        'freq': freq,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'index.html', context)

@login_required(login_url='/')
def request_pending(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_pending.html', context)

@login_required(login_url='/')
def request_history(request, freq, fstatus, fstartdate, fstopdate):
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
    return render(request, 'request_history.html', context)

#----------------------------------- Master -----------------------------------#

@login_required(login_url='/')
def master_emp(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_emp.html', context)

@login_required(login_url='/')
def master_mc(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_mc.html', context)

@login_required(login_url='/')
def master_vendor(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_vendor.html', context)

@login_required(login_url='/')
def master_cat(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_cat.html', context)

#---------------------------------- New Data ----------------------------------#

@login_required(login_url='/')
def new_emp(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_emp.html', context)

@login_required(login_url='/')
def new_mc(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_mc.html', context)

@login_required(login_url='/')
def new_vendor(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_vendor.html', context)

@login_required(login_url='/')
def new_cat(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_cat.html', context)

################################### Request ####################################

def new_emp_save(request):
    username = request.POST['new_username']
    password = request.POST['new_password']
    name = request.POST['name']
    section = request.POST['section']
    view_type = request.POST['view_type']
    phone_no = request.POST['phone_no']
    user_new = User.objects.create_user(username, '', password)
    user_new.save()
    employee_new = Employee(user=user_new,name=name,section=section,view_type=view_type,phone_no=phone_no)
    employee_new.save()
    return redirect('/new_emp/')

def validate_username(request):
    canUse = True
    username = request.GET['username']
    isExist = User.objects.filter(username=username).exists()
    if isExist:
        canUse = False
    data = {
        'canUse': canUse,
    }
    return JsonResponse(data)
