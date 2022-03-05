from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from dateutil import parser
# Authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# File Reader
from openpyxl import load_workbook, Workbook

from .models import Employee, Machine

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
    ma_mcs = Machine.objects.filter(is_active=True, mc_of='MA').order_by('section')
    ad_ser_mcs = Machine.objects.filter(is_active=True, mc_of='AD-SER').order_by('section')
    ma_section_group = get_section_group(ma_mcs)
    ad_ser_section_group = get_section_group(ad_ser_mcs)
    context = {
        'ma_mcs': ma_mcs,
        'ad_ser_mcs': ad_ser_mcs,
        'ma_section_group': ma_section_group,
        'ad_ser_section_group': ad_ser_section_group,
    }
    return render(request, 'new_request.html', context)

def new_pv_request(request):
    mcs = []
    if request.user.employee.view_type == 'MA':
        mcs = Machine.objects.filter(is_active=True, mc_of='MA').order_by('section')
    elif request.user.employee.view_type == 'AD_SER':
        mcs = Machine.objects.filter(is_active=True, mc_of='AD-SER').order_by('section')
    else:
        mcs = Machine.objects.filter(is_active=True).order_by('section')
    section_group = get_section_group(mcs)
    context = {
        'mcs': mcs,
        'section_group': section_group,
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
def request_pending(request, freq):
    context = {
        'freq': freq,
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
    mcs = Machine.objects.all()
    context = {
        'mcs': mcs,
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
    # upload_machine()
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

#################################### OTHER #####################################

def get_section_group(mcs):
    section_group = []
    temp = ""
    for mc in mcs:
        if temp != mc.section:
            temp = mc.section
            section_group.append(mc.section)
        else:
            section_group.append(None)
    return section_group

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

################################# File Reader ##################################

def upload_machine():
    entries = Machine.objects.all()
    entries.delete()
    wb = load_workbook(filename = 'media/CMS Machine Master.xlsx')
    ws = wb.active
    skip_count = 2
    for i in range(ws.max_row + 1):
        if i < skip_count:
            continue
        mc_of = 'MA'
        section = ws['A' + str(i)].value
        register_no = ws['B' + str(i)].value
        mc_no = ws['C' + str(i)].value
        asset_no = ws['D' + str(i)].value
        manufacture = ws['E' + str(i)].value
        plant = ws['F' + str(i)].value
        model = ws['G' + str(i)].value
        serial_no = ws['H' + str(i)].value
        capacity = ws['I' + str(i)].value
        power  = ws['J' + str(i)].value
        install_date = ws['K' + str(i)].value
        note = ws['L' + str(i)].value
        if mc_no != None and mc_no != "":
            print(mc_no)
            mc_new = Machine(mc_no=mc_no,mc_of=mc_of,section=section,register_no=register_no,asset_no=asset_no,serial_no=serial_no,manufacture=manufacture,model=model,plant=plant,power=power,install_date=install_date,capacity=capacity,note=note)
            mc_new.save()
    return
