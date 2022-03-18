from django.shortcuts import render, redirect
from django.http import JsonResponse
from dateutil import parser
# Authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# File Reader
from openpyxl import load_workbook, Workbook
# Date Time
from datetime import datetime, timedelta
# EMAIL
from django.core.mail import EmailMessage
from cms.settings import EMAIL_HOST_USER
import smtplib
import traceback
import threading
from django.template.loader import get_template
# File
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import glob, os, shutil
# Token Generator
import secrets

from .models import SectionGroup, Employee, Machine, Task, Vendor, Category, SubCategory, MailGroup, Request, File, Member, RequestVendor, Comment, RequestSubCategory, OperatorWorkingTime, VendorWorkingTime, MachineDowntime

HOST_URL = 'http://129.1.100.185:8200/'
TEMPLATE_REQUEST = 'email_templates/request.html'

################################# Authenticate #################################

def first_page(request):
    sgs = SectionGroup.objects.all()
    context = {
        'sgs': sgs,
    }
    return render(request, 'first_page.html', context)

def track_request(request, search_text):
    reqs = []
    if search_text != '0':
        reqs = Request.objects.filter(type="User Request",emp_id=search_text).order_by('-request_date')[:12]
    else:
        search_text = ""
    context = {
        'search_text': search_text,
        'reqs': reqs,
    }
    return render(request, 'track_request.html', context)

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
        return redirect('/index/')
    return redirect('/')

@login_required(login_url='/')
def logout_action(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def setting(request):
    # upload_machine()
    #upload_task()
    upload_vendor()
    users = []
    user_group = []
    if request.user.is_superuser or request.user.is_staff:
        users = sort_user_by_section(User.objects.all())
        user_group = get_user_group(users)
    context = {
        'users': users,
        'user_group': user_group,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'setting.html', context)

##################################### Page #####################################

def new_request(request):
    sgs = SectionGroup.objects.all()
    token = secrets.token_urlsafe(16)
    context = {
        'sgs': sgs,
        'token': token,
    }
    return render(request, 'new_request.html', context)

def new_request_success(request, request_no):
    context = {
        'request_no': request_no,
    }
    return render(request, 'new_request_success.html', context)

def new_pv_request(request):
    sgs = SectionGroup.objects.all()
    mcs = Machine.objects.filter(is_active=True).order_by('section')
    tasks = Task.objects.filter(is_active=True).order_by('type')
    mc_group = get_mc_group(mcs)
    task_group = get_task_group(tasks)
    token = secrets.token_urlsafe(16)
    context = {
        'sgs': sgs,
        'mcs': mcs,
        'tasks': tasks,
        'mc_group': mc_group,
        'task_group': task_group,
        'token': token,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_pv_request.html', context)

def edit_request(request,  request_no):
    req = Request.objects.get(req_no=request_no)
    mcs = Machine.objects.filter(is_active=True).order_by('section')
    token = secrets.token_urlsafe(16)
    context = {
        'request_no': request_no,
        'req': req,
        'mcs': mcs,
        'token': token,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'edit_request.html', context)

@login_required(login_url='/')
def request_page(request, request_no):
    req_is_exist = Request.objects.filter(req_no=request_no).exists()
    req = None
    is_member = False
    members = [] # Member (User)
    files = []
    req_vens = [] # RequestVendor
    comments = [] # Comment
    req_sub_cats = [] # RequestSubCategory
    req_sub_cat_group = [] # RequestSubCategory Group (Category)
    files = [] # Files
    owts = [] # OpereatorWorkTime
    vwts = [] # VendorWorkingTime
    mcdts = [] # MachineDowntime
    wt_len = 0

    sgs = [] # All Available SectionGroup
    mcs = [] # All Available Machine
    users = [] # All Available User
    vens = [] # All Available Vendor
    sub_cats = [] # All Available SubCategory

    mc_group = [] # Machine Group (Section)
    user_group = [] # User Group (Section)
    sub_cat_group = [] # SubCategory Group (Category)

    select_members = [] # For Manage Member
    select_vendors = [] # For Manage Vendor
    select_sub_cats = [] # For Manage Category
    if req_is_exist:
        req = Request.objects.get(req_no=request_no)
        is_member = Member.objects.filter(req=req,user=request.user).exists()
        members = Member.objects.filter(req=req)
        files = File.objects.filter(req=req)
        req_vens = RequestVendor.objects.filter(req=req)
        comments = Comment.objects.filter(req=req).order_by('-date_published')
        req_sub_cats = RequestSubCategory.objects.filter(req=req)
        req_sub_cat_group = get_req_sub_cat_group(req_sub_cats)
        files = File.objects.filter(req=req)
        owts = OperatorWorkingTime.objects.filter(req=req).order_by('-start_datetime')
        vwts = VendorWorkingTime.objects.filter(req=req).order_by('-start_datetime')
        mcdts = MachineDowntime.objects.filter(req=req).order_by('-start_datetime')
        wt_len = len(owts) + len(vwts)
        sgs = SectionGroup.objects.all()
        mcs = Machine.objects.filter(is_active=True).order_by('section')
        users = sort_user_by_section(User.objects.filter(is_active=True))
        vens = Vendor.objects.filter(is_active=True)
        sub_cats = SubCategory.objects.all().order_by('cat')
        mc_group = get_mc_group(mcs)
        user_group = get_user_group(users)
        sub_cat_group = get_sub_cat_group(sub_cats)
        select_members = get_select_members(req, users)
        select_vendors = get_select_vendors(req, vens)
        select_sub_cats = get_select_sub_cats(req, sub_cats)
    context = {
        'request_no': request_no,
        'req_is_exist': req_is_exist,
        'req': req,
        'is_member': is_member,
        'members': members,
        'files': files,
        'req_vens': req_vens,
        'comments': comments,
        'req_sub_cats': req_sub_cats,
        'req_sub_cat_group': req_sub_cat_group,
        'files': files,
        'owts': owts,
        'vwts': vwts,
        'mcdts': mcdts,
        'wt_len': wt_len,
        'sgs': sgs,
        'mcs': mcs,
        'users': users,
        'vens': vens,
        'sub_cats': sub_cats,
        'mc_group': mc_group,
        'user_group': user_group,
        'sub_cat_group': sub_cat_group,
        'select_members': select_members,
        'select_vendors': select_vendors,
        'select_sub_cats': select_sub_cats,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_page.html', context)

#------------------------------------ Main ------------------------------------#

def all_page_data(request):
    is_in = is_in_section_group(request)
    my_reqs = []
    temp_reqs = Request.objects.filter(status='On Progress') | Request.objects.filter(status='On Hold')
    for req in temp_reqs:
        is_member = Member.objects.filter(req=req,user=request.user).exists()
        if is_member:
            my_reqs.append(req)
    my_request_count = len(my_reqs)

    pending_reqs = []
    if is_in_section_group(request):
        pending_reqs = Request.objects.filter(status='Pending',sg=request.user.employee.section)
    else :
        pending_reqs = Request.objects.filter(status='Pending')
    pending_request_count = len(pending_reqs)

    all_reqs = []
    if is_in_section_group(request):
        all_reqs = Request.objects.filter(status='On Progress',sg=request.user.employee.section) | Request.objects.filter(status='On Hold',sg=request.user.employee.section)
    else :
        all_reqs = Request.objects.filter(status='On Progress') | Request.objects.filter(status='On Hold')
    all_request_count = len(all_reqs)
    context = {
        'is_in': is_in,
        'my_request_count': my_request_count,
        'pending_request_count': pending_request_count,
        'all_request_count': all_request_count,
    }
    return context

@login_required(login_url='/')
def index(request):
    reqs = []
    temp_reqs = Request.objects.filter(status='On Progress') | Request.objects.filter(status='On Hold')
    for req in temp_reqs:
        is_member = Member.objects.filter(req=req,user=request.user).exists()
        if is_member:
            reqs.append(req)
    context = {
        'reqs': reqs,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'index.html', context)

@login_required(login_url='/')
def request_pending(request, fsg):
    sgs = SectionGroup.objects.all()
    reqs = []
    if fsg == 'MY' and is_in_section_group(request):
        fsg = request.user.employee.section
    elif fsg == 'MY':
        fsg = 'ALL'
    if fsg == 'ALL':
        reqs = Request.objects.filter(status='Pending')
    else:
        reqs = Request.objects.filter(status='Pending',sg=fsg)
    context = {
        'sgs': sgs,
        'fsg': fsg,
        'reqs': reqs,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_pending.html', context)

@login_required(login_url='/')
def request_all(request, fsg):
    sgs = SectionGroup.objects.all()
    reqs = []
    if fsg == 'MY' and is_in_section_group(request):
        fsg = request.user.employee.section
    elif fsg == 'MY':
        fsg = 'ALL'
    if fsg == 'ALL':
        reqs = Request.objects.filter(status='On Progress')  | Request.objects.filter(status='On Hold')
    else:
        reqs = Request.objects.filter(status='On Progress',sg=fsg)  | Request.objects.filter(status='On Hold',sg=fsg)
    is_members = get_is_members(reqs, request)
    context = {
        'sgs': sgs,
        'fsg': fsg,
        'reqs': reqs,
        'is_members': is_members,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_all.html', context)

@login_required(login_url='/')
def request_history(request, fsg, fstartdate, fstopdate):
    sgs = SectionGroup.objects.all()
    reqs = []
    if fsg == 'MY' and is_in_section_group(request):
        fsg = request.user.employee.section
    elif fsg == 'MY':
        fsg = 'ALL'
    if fstartdate == "LASTWEEK":
        fstartdate = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    if fstopdate == "TODAY":
        fstopdate = datetime.today().strftime('%Y-%m-%d')
    if fsg == 'ALL':
        reqs = Request.objects.filter(status='Rejected',finish_datetime__date__range=[fstartdate, fstopdate])  | Request.objects.filter(status='Complete',finish_datetime__date__range=[fstartdate, fstopdate]) | Request.objects.filter(status='Canceled',finish_datetime__date__range=[fstartdate, fstopdate])
    else:
        reqs = Request.objects.filter(status='Rejected',sg=fsg,finish_datetime__date__range=[fstartdate, fstopdate])  | Request.objects.filter(status='Complete',sg=fsg,finish_datetime__date__range=[fstartdate, fstopdate]) | Request.objects.filter(status='Canceled',sg=fsg,finish_datetime__date__range=[fstartdate, fstopdate])
    is_members = get_is_members(reqs, request)
    context = {
        'sgs': sgs,
        'fsg': fsg,
        'fstartdate': fstartdate,
        'fstopdate': fstopdate,
        'reqs': reqs,
        'is_members': is_members,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_history.html', context)

#----------------------------------- Report -----------------------------------#

@login_required(login_url='/')
def summary(request, fsg):
    sgs = SectionGroup.objects.all()
    pending_req_count = 0
    rejected_req_count = 0
    on_process_req_count = 0
    on_hold_req_count = 0
    complete_req_count = 0
    canceled_req_count = 0

    pending_us_req_count = 0
    rejected_us_req_count = 0
    on_process_us_req_count = 0
    on_hold_us_req_count = 0
    complete_us_req_count = 0
    canceled_us_req_count = 0

    pending_pv_req_count = 0
    rejected_pv_req_count = 0
    on_process_pv_req_count = 0
    on_hold_pv_req_count = 0
    complete_pv_req_count = 0
    canceled_pv_req_count = 0
    if fsg == 'MY' and is_in_section_group(request):
        fsg = request.user.employee.section
    elif fsg == 'MY':
        fsg = 'ALL'
    if fsg == 'ALL':
        pending_us_req_count = len(Request.objects.filter(status='Pending',type='User Request'))
        pending_pv_req_count = len(Request.objects.filter(status='Pending',type='Preventive'))
        pending_req_count = pending_us_req_count + pending_pv_req_count
        rejected_us_req_count = len(Request.objects.filter(status='Rejected',type='User Request'))
        rejected_pv_req_count = len(Request.objects.filter(status='Rejected',type='Preventive'))
        rejected_req_count = rejected_us_req_count + rejected_pv_req_count
        on_process_us_req_count = len(Request.objects.filter(status='On Progress',type='User Request'))
        on_process_pv_req_count = len(Request.objects.filter(status='On Progress',type='Preventive'))
        on_process_req_count = on_process_us_req_count + on_process_pv_req_count
        on_hold_us_req_count = len(Request.objects.filter(status='On Hold',type='User Request'))
        on_hold_pv_req_count = len(Request.objects.filter(status='On Hold',type='Preventive'))
        on_hold_req_count = on_hold_us_req_count + on_hold_pv_req_count
        complete_us_req_count = len(Request.objects.filter(status='Complete',type='User Request'))
        complete_pv_req_count = len(Request.objects.filter(status='Complete',type='Preventive'))
        complete_req_count = complete_us_req_count + complete_pv_req_count
        canceled_us_req_count = len(Request.objects.filter(status='Canceled',type='User Request'))
        canceled_pv_req_count = len(Request.objects.filter(status='Canceled',type='Preventive'))
        canceled_req_count = canceled_us_req_count + canceled_pv_req_count
    else:
        pending_us_req_count = len(Request.objects.filter(status='Pending',type='User Request',sg=fsg))
        pending_pv_req_count = len(Request.objects.filter(status='Pending',type='Preventive',sg=fsg))
        pending_req_count = pending_us_req_count + pending_pv_req_count
        rejected_us_req_count = len(Request.objects.filter(status='Rejected',type='User Request',sg=fsg))
        rejected_pv_req_count = len(Request.objects.filter(status='Rejected',type='Preventive',sg=fsg))
        rejected_req_count = rejected_us_req_count + rejected_pv_req_count
        on_process_us_req_count = len(Request.objects.filter(status='On Progress',type='User Request',sg=fsg))
        on_process_pv_req_count = len(Request.objects.filter(status='On Progress',type='Preventive',sg=fsg))
        on_process_req_count = on_process_us_req_count + on_process_pv_req_count
        on_hold_us_req_count = len(Request.objects.filter(status='On Hold',type='User Request',sg=fsg))
        on_hold_pv_req_count = len(Request.objects.filter(status='On Hold',type='Preventive',sg=fsg))
        on_hold_req_count = on_hold_us_req_count + on_hold_pv_req_count
        complete_us_req_count = len(Request.objects.filter(status='Complete',type='User Request',sg=fsg))
        complete_pv_req_count = len(Request.objects.filter(status='Complete',type='Preventive',sg=fsg))
        complete_req_count = complete_us_req_count + complete_pv_req_count
        canceled_us_req_count = len(Request.objects.filter(status='Canceled',type='User Request',sg=fsg))
        canceled_pv_req_count = len(Request.objects.filter(status='Canceled',type='Preventive',sg=fsg))
        canceled_req_count = canceled_us_req_count + canceled_pv_req_count
    context = {
        'sgs': sgs,
        'fsg': fsg,
        'pending_req_count': pending_req_count,
        'rejected_req_count': rejected_req_count,
        'on_process_req_count': on_process_req_count,
        'on_hold_req_count': on_hold_req_count,
        'complete_req_count': complete_req_count,
        'canceled_req_count': canceled_req_count,

        'pending_us_req_count': pending_us_req_count,
        'rejected_us_req_count': rejected_us_req_count,
        'on_process_us_req_count': on_process_us_req_count,
        'on_hold_us_req_count': on_hold_us_req_count,
        'complete_us_req_count': complete_us_req_count,
        'canceled_us_req_count': canceled_us_req_count,

        'pending_pv_req_count': pending_pv_req_count,
        'rejected_pv_req_count': rejected_pv_req_count,
        'on_process_pv_req_count': on_process_pv_req_count,
        'on_hold_pv_req_count': on_hold_pv_req_count,
        'complete_pv_req_count': complete_pv_req_count,
        'canceled_pv_req_count': canceled_pv_req_count,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'summary.html', context)

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
def master_task(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_task.html', context)

@login_required(login_url='/')
def master_ven(request):
    vens = Vendor.objects.all()
    context = {
        'vens': vens,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_ven.html', context)

@login_required(login_url='/')
def master_cat(request):
    cats = Category.objects.all()
    context = {
        'cats': cats,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_cat.html', context)

@login_required(login_url='/')
def master_sub_cat(request):
    sub_cats = SubCategory.objects.all()
    context = {
        'sub_cats': sub_cats,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_sub_cat.html', context)

@login_required(login_url='/')
def master_sg(request):
    sgs = SectionGroup.objects.all()
    context = {
        'sgs': sgs,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_sg.html', context)

@login_required(login_url='/')
def master_mg(request):
    mgs = MailGroup.objects.all()
    context = {
        'mgs': mgs,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_mg.html', context)

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
def new_task(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_task.html', context)

@login_required(login_url='/')
def new_ven(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_ven.html', context)

@login_required(login_url='/')
def new_cat(request):
    context = {
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_cat.html', context)

@login_required(login_url='/')
def new_sub_cat(request):
    cats = Category.objects.all()
    context = {
        'cats': cats,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_sub_cat.html', context)

@login_required(login_url='/')
def new_mg(request):
    sgs = SectionGroup.objects.all()
    users = sort_user_by_section(User.objects.all())
    user_group = get_user_group(users)
    context = {
        'sgs': sgs,
        'users': users,
        'user_group': user_group,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_mg.html', context)

#--------------------------------- Edit Data ----------------------------------#

@login_required(login_url='/')
def edit_mc(request, fmc):
    mcs = Machine.objects.all().order_by('section')
    mc_group = get_mc_group(mcs)
    if fmc == 'FIRST':
        fmc = mcs[0].mc_no
    mc = Machine.objects.get(mc_no=fmc)
    context = {
        'fmc': fmc,
        'mcs': mcs,
        'mc_group': mc_group,
        'mc': mc,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'edit_mc.html', context)

@login_required(login_url='/')
def edit_task(request, ftask):
    tasks = Task.objects.all().order_by('type')
    task_group = get_task_group(tasks)
    if ftask == 'FIRST':
        ftask = tasks[0].id
    task = Task.objects.get(id=ftask)
    context = {
        'ftask': ftask,
        'tasks': tasks,
        'task_group': task_group,
        'task': task,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'edit_task.html', context)

@login_required(login_url='/')
def edit_ven(request, fven):
    vens = Vendor.objects.all().order_by('code')
    if fven == 'FIRST':
        fven = vens[0].code
    ven = Vendor.objects.get(code=fven)
    context = {
        'fven': fven,
        'vens': vens,
        'ven': ven,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'edit_ven.html', context)

#################################### POST ######################################
def setting_save(request):
    is_reset = True if request.POST.get('is_reset', False) == 'on' else False
    new_password = request.POST['new_password']
    name = request.POST['name']
    section = request.POST['section']
    email = request.POST['email']
    phone_no = request.POST['phone_no']
    scheme = request.POST['scheme']
    sidebar = request.POST['sidebar']
    pv_created = request.POST['pv_created']
    auto_add = request.POST['auto_add']
    default_owt = request.POST['default_owt']
    reset_password_username = request.POST['reset_password_username'] if request.POST['reset_password_username'] != 'Select' else None
    user = request.user
    user.email = email
    if(is_reset):
        user.set_password(new_password)
    user.save()
    emp = request.user.employee
    emp.name = name
    emp.section = section
    emp.phone_no = phone_no
    emp.scheme = scheme
    emp.sidebar = sidebar
    emp.pv_created = pv_created
    emp.auto_add = auto_add
    emp.default_owt = default_owt
    emp.save()
    #-- Admin Function
    if reset_password_username != None:
        u = User.objects.get(username=reset_password_username)
        u.set_password('Ccs.1234')
        u.save()
    return redirect('/setting/')

def new_request_save(request):
    token = request.POST['token']
    emp_id = request.POST['emp_id'].strip()
    name = request.POST['name'].strip()
    section = request.POST['section'].strip()
    email = request.POST['email'].strip()
    phone_no = request.POST['phone_no'].strip()
    sg_name = request.POST['sg_name']
    description = request.POST['description']
    cc_to_me = True if request.POST.get('cc_to_me', False) == 'on' else False
    type = 'User Request'
    status = 'Pending'
    request_date = datetime.now().date()
    sg = SectionGroup.objects.get(name=sg_name)
    request_new = Request(emp_id=emp_id,name=name,section=section,email=email,phone_no=phone_no,sg=sg,type=type,status=status,request_date=request_date,description=description)
    request_new.save()
    request_new.req_no = create_req_no(request_new.id)
    request_new.save()
    #-- File Manage
    source_dir = 'media/temp/' + token
    target_dir = 'media/request/' + request_new.req_no
    try:
        os.listdir(source_dir)
        os.mkdir(target_dir)
    except:
        print('No File Upload')
    try:
        for file_name in os.listdir(source_dir):
            shutil.move(os.path.join(source_dir, file_name), os.path.join(target_dir))
            file_new = File(req=request_new,file_name=file_name)
            file_new.save()
        shutil.rmtree(source_dir, ignore_errors=False, onerror=None)
    except:
        print('Path Not Found')
    #-- Email
    subject = '[CMS] New Request #' + request_new.req_no
    send_to = get_mail_group(sg, False)
    cc_to = get_mail_group(sg, True)
    if cc_to_me:
        cc_to.append(request_new.email)
    email_template = get_template(TEMPLATE_REQUEST)
    email_content = email_template.render({
        'type' : 'New Request',
        'req' : request_new,
        'host_url' : HOST_URL,
    })
    # send_email(subject, email_content, send_to, cc_to)
    return redirect('/new_request_success/' + request_new.req_no)

def new_pv_request_save(request):
    token = request.POST['token']
    sg_name = request.POST['sg_name']
    request_date = request.POST['req_date']
    description = request.POST['description']
    obj_type = request.POST['obj_type']
    mc_no = request.POST['mc_no'] if request.POST['obj_type'] == 'MACHINE' else None
    task_id = request.POST['task_id'] if request.POST['obj_type'] == 'TASK' else None
    mc = None
    if mc_no != None:
        mc = Machine.objects.get(mc_no=mc_no)
    task = None
    if task_id != None:
        task = Task.objects.get(id=task_id)
    type = 'Preventive'
    status = 'Pending'
    sg = SectionGroup.objects.get(name=sg_name)
    emp_id = request.user.username
    name = request.user.employee.name
    section = request.user.employee.section
    email = request.user.email
    phone_no = request.user.employee.phone_no
    request_new = Request(emp_id=emp_id,name=name,section=section,email=email,phone_no=phone_no,sg=sg,type=type,status=status,request_date=request_date,description=description,mc=mc,task=task)
    request_new.save()
    request_new.req_no = create_req_no(request_new.id)
    request_new.save()
    #-- File Manage
    source_dir = 'media/temp/' + token
    target_dir = 'media/request/' + request_new.req_no
    try:
        os.listdir(source_dir)
        os.mkdir(target_dir)
    except:
        print('No File Upload')
    try:
        for file_name in os.listdir(source_dir):
            shutil.move(os.path.join(source_dir, file_name), os.path.join(target_dir))
            file_new = File(req=request_new,file_name=file_name)
            file_new.save()
        shutil.rmtree(source_dir, ignore_errors=False, onerror=None)
    except:
        print('Path Not Found')
    #-- Navigate
    if request.user.employee.pv_created == 'Request Page':
        return redirect('/request_page/' + request_new.req_no)
    return redirect('/new_pv_request/')

def edit_request_save(request):
    token = request.POST['token']
    req_id = request.POST['req_id']
    request_date = request.POST['req_date']
    description = request.POST['description']
    mc_no = request.POST['mc_no'] if request.POST['mc_no'] != 'Select' else None
    mc = None
    is_same_mc = False
    req = Request.objects.get(id=req_id)
    if mc_no != None:
        mc = Machine.objects.get(mc_no=mc_no)
        if req.mc == mc:
            is_same_mc = True
    req.request_date = request_date
    req.mc = mc
    req.description = description
    if not is_same_mc:
        mcdts = MachineDowntime.objects.filter(req=req)
        mcdts.delete()
    req.save()
    #-- File Manage
    source_dir = 'media/temp/' + token
    target_dir = 'media/request/' + req.req_no
    try:
        os.listdir(source_dir)
        try:
            os.mkdir(target_dir)
        except:
            print('Folder is already Exist')
        try:
            for file_name in os.listdir(source_dir):
                shutil.move(os.path.join(source_dir, file_name), os.path.join(target_dir))
                file_new = File(req=req,file_name=file_name)
                file_new.save()
            shutil.rmtree(source_dir, ignore_errors=False, onerror=None)
        except:
            print('Path Not Found')
    except:
        print('No File Upload')
    return redirect('/request_page/' + req.req_no)

def new_emp_save(request):
    username = request.POST['new_username'].strip()
    password = request.POST['new_password']
    name = request.POST['name'].strip()
    section = request.POST['section'].strip()
    email = request.POST['email'].strip()
    phone_no = request.POST['phone_no'].strip()
    user_new = User.objects.create_user(username, '', password)
    user_new.email = email
    user_new.save()
    employee_new = Employee(user=user_new,name=name,section=section,phone_no=phone_no)
    employee_new.save()
    return redirect('/new_emp/')

def new_mc_save(request):
    mc_no = request.POST['mc_no'].strip()
    section = request.POST['section'].strip()
    register_no = request.POST['register_no'].strip()
    asset_no = request.POST['asset_no'].strip()
    serial_no = request.POST['serial_no'].strip()
    manufacture = request.POST['manufacture'].strip()
    model = request.POST['model'].strip()
    plant = request.POST['plant'].strip()
    power = request.POST['power'].strip()
    install_date = request.POST['install_date'] if request.POST['install_date'] != "" else None
    capacity = request.POST['capacity']
    note = request.POST['note']
    mc_new = Machine(mc_no=mc_no,section=section,register_no=register_no,asset_no=asset_no,serial_no=serial_no,manufacture=manufacture,model=model,plant=plant,power=power,install_date=install_date,capacity=capacity,note=note)
    mc_new.save()
    return redirect('/new_mc/')

def new_task_save(request):
    type = request.POST['type'].strip()
    name = request.POST['name'].strip()
    note = request.POST['note']
    task_new = Task(type=type,name=name,note=note)
    task_new.save()
    return redirect('/new_task/')

def new_ven_save(request):
    code = request.POST['code'].strip()
    name = request.POST['name'].strip()
    address = request.POST['address']
    email = request.POST['email'].strip()
    phone_no = request.POST['phone_no'].strip()
    note = request.POST['note']
    ven_new = Vendor(code=code,name=name,address=address,email=email,phone_no=phone_no,note=note)
    ven_new.save()
    return redirect('/new_ven/')

def new_cat_save(request):
    name = request.POST['name'].strip()
    cat_new = Category(name=name)
    cat_new.save()
    return redirect('/new_cat/')

def new_sub_cat_save(request):
    name = request.POST['name'].strip()
    cat_id = request.POST['cat_id']
    description = request.POST['description']
    cat = Category.objects.get(id=cat_id)
    sub_cat_new = SubCategory(name=name,cat=cat,description=description)
    sub_cat_new.save()
    return redirect('/new_sub_cat/')

def new_mg_save(request):
    sg_name = request.POST['sg_name']
    username = request.POST['username']
    is_cc = True if request.POST.get('is_cc', False) == 'on' else False
    sg = SectionGroup.objects.get(name=sg_name)
    user = User.objects.get(username=username)
    mg_new = MailGroup(sg=sg,user=user,is_cc=is_cc)
    mg_new.save()
    return redirect('/new_mg/')

def edit_mc_save(request):
    is_active = True if request.POST.get('is_active', False) == 'on' else False
    mc_no = request.POST['mc_no']
    register_no = request.POST['register_no'].strip()
    asset_no = request.POST['asset_no'].strip()
    serial_no = request.POST['serial_no'].strip()
    manufacture = request.POST['manufacture'].strip()
    model = request.POST['model'].strip()
    plant = request.POST['plant'].strip()
    power = request.POST['power'].strip()
    install_date = request.POST['install_date'] if request.POST['install_date'] != "" else None
    capacity = request.POST['capacity']
    note = request.POST['note']
    mc = Machine.objects.get(mc_no=mc_no)
    mc.is_active = is_active
    mc.register_no = register_no
    mc.asset_no = asset_no
    mc.serial_no = serial_no
    mc.manufacture = manufacture
    mc.model = model
    mc.plant = plant
    mc.power = power
    mc.install_date = install_date
    mc.capacity = capacity
    mc.note = note
    mc.save()
    return redirect('/edit_mc/' + mc.mc_no)

def edit_task_save(request):
    is_active = True if request.POST.get('is_active', False) == 'on' else False
    id = request.POST['id']
    note = request.POST['note']
    task = Task.objects.get(id=id)
    task.is_active = is_active
    task.note = note
    task.save()
    return redirect('/edit_task/' + str(task.id))

def edit_ven_save(request):
    is_active = True if request.POST.get('is_active', False) == 'on' else False
    code = request.POST['code']
    address = request.POST['address']
    email = request.POST['email']
    phone_no = request.POST['phone_no']
    note = request.POST['note']
    ven = Vendor.objects.get(code=code)
    ven.is_active = is_active
    ven.address = address
    ven.email = email
    ven.phone_no = phone_no
    ven.note = note
    ven.save()
    return redirect('/edit_ven/' + str(ven.code))

def file_save(request):
    file = request.FILES['file']
    token = request.POST['token']
    fs = FileSystemStorage()
    path = 'temp/' + token + '/' + file.name
    fs.save(path, file)
    data = {
    }
    return JsonResponse(data)

##################################### GET ######################################

def validate_old_password(request):
    username = request.GET['username']
    old_password = request.GET['old_password']
    isCorrect = True
    user = authenticate(request,username=username,password=old_password)
    if user == None:
        isCorrect = False
    data = {
        'isCorrect': isCorrect,
    }
    return JsonResponse(data)

def validate_username(request):
    username = request.GET['username']
    canUse = True
    isExist = User.objects.filter(username=username).exists()
    if isExist:
        canUse = False
    data = {
        'canUse': canUse,
    }
    return JsonResponse(data)

def validate_mc_no(request):
    mc_no = request.GET['mc_no'].strip()
    canUse = True
    isExist = Machine.objects.filter(mc_no__iexact=mc_no).exists()
    if isExist:
        canUse = False
    data = {
        'canUse': canUse,
    }
    return JsonResponse(data)

def validate_task(request):
    type = request.GET['type'].strip()
    name = request.GET['name'].strip()
    canUse = True
    isExist = Task.objects.filter(name__iexact=name,type__iexact=type).exists()
    if isExist:
        canUse = False
    data = {
        'canUse': canUse,
    }
    return JsonResponse(data)

def validate_vendor_code(request):
    code = request.GET['code'].strip()
    canUse = True
    isExist = Vendor.objects.filter(code__iexact=code).exists()
    if isExist:
        canUse = False
    data = {
        'canUse': canUse,
    }
    return JsonResponse(data)

def validate_category_name(request):
    name = request.GET['name'].strip()
    canUse = True
    isExist = Category.objects.filter(name__iexact=name).exists()
    if isExist:
        canUse = False
    data = {
        'canUse': canUse,
    }
    return JsonResponse(data)

def validate_sub_category_name(request):
    name = request.GET['name'].strip()
    cat_id = request.GET['cat_id']
    canUse = True
    cat = Category.objects.get(id=cat_id)
    isExist = SubCategory.objects.filter(name__iexact=name,cat=cat).exists()
    if isExist:
        canUse = False
    data = {
        'canUse': canUse,
    }
    return JsonResponse(data)

def validate_user_in_mailgroup(request):
    sg_name = request.GET['sg_name']
    username = request.GET['username']
    canUse = True
    sg = SectionGroup.objects.get(name=sg_name)
    user = User.objects.get(username=username)
    isExist = MailGroup.objects.filter(sg=sg,user=user).exists()
    if isExist:
        canUse = False
    data = {
        'canUse': canUse,
    }
    return JsonResponse(data)

def find_emp_info(request):
    emp_id = request.GET['emp_id']
    found = False
    name = ""
    section = ""
    email = ""
    phone_no = ""
    reqs = Request.objects.filter(emp_id=emp_id).order_by('-date_published')
    if reqs:
        found = True
        name = reqs[0].name
        section = reqs[0].section
        email = reqs[0].email
        phone_no = reqs[0].phone_no
    data = {
        'found': found,
        'name': name,
        'section': section,
        'email': email,
        'phone_no': phone_no,
    }
    return JsonResponse(data)

def accept_request(request):
    req_id = request.GET['req_id']
    mc_no = request.GET['mc_no'] if request.GET['mc_no'] != 'Select' else None
    username_list = request.GET.getlist('username_list[]')
    ven_code_list = request.GET.getlist('ven_code_list[]')
    sub_cat_id_list = request.GET.getlist('sub_cat_id_list[]')
    req = Request.objects.get(id=req_id)
    if mc_no != None:
        mc = Machine.objects.get(mc_no=mc_no)
        req.mc = mc
    for username in username_list:
        user = User.objects.get(username=username)
        member_new = Member(req=req,user=user)
        member_new.save()
    for ven_code in ven_code_list:
        ven = Vendor.objects.get(code=ven_code)
        req_ven_new = RequestVendor(req=req,ven=ven)
        req_ven_new.save()
    for sub_cat_id in sub_cat_id_list:
        sub_cat = SubCategory.objects.get(id=sub_cat_id)
        req_sub_cat_new = RequestSubCategory(req=req,sub_cat=sub_cat)
        req_sub_cat_new.save()
    req.status = 'On Progress'
    req.save()
    data = {
    }
    return JsonResponse(data)

def reject_request(request):
    req_id = request.GET['req_id']
    is_nms = True if request.GET['is_nms'] == 'true' else False
    reject_reason = request.GET['reject_reason']
    sg_name = request.GET['sg_name']
    req = Request.objects.get(id=req_id)
    if is_nms:
        sg = SectionGroup.objects.get(name=sg_name)
        req.sg = sg
    else:
        req.status = 'Rejected'
        req.reason = reject_reason
        req.finish_datetime = datetime.now()
    req.save()
    data = {
    }
    return JsonResponse(data)

def join_request(request):
    req_id = request.GET['req_id']
    req = Request.objects.get(id=req_id)
    member_new = Member(req=req,user=request.user)
    member_new.save()
    data = {
    }
    return JsonResponse(data)

def leave_request(request):
    req_id = request.GET['req_id']
    req = Request.objects.get(id=req_id)
    member = Member.objects.get(req=req,user=request.user)
    member.delete()
    data = {
    }
    return JsonResponse(data)

def hold_request(request):
    req_id = request.GET['req_id']
    hold_reason = request.GET['hold_reason']
    req = Request.objects.get(id=req_id)
    req.status = 'On Hold'
    req.reason = hold_reason
    req.save()
    data = {
    }
    return JsonResponse(data)

def start_work_request(request):
    req_id = request.GET['req_id']
    req = Request.objects.get(id=req_id)
    req.status = 'On Progress'
    req.reason = None
    req.save()
    data = {
    }
    return JsonResponse(data)

def complete_request(request):
    req_id = request.GET['req_id']
    req = Request.objects.get(id=req_id)
    req.status = 'Complete'
    req.reason = None
    req.finish_datetime = datetime.now()
    req.save()
    data = {
    }
    return JsonResponse(data)

def cancel_request(request):
    req_id = request.GET['req_id']
    cancel_reason = request.GET['cancel_reason']
    req = Request.objects.get(id=req_id)
    req.status = 'Canceled'
    req.reason = cancel_reason
    req.finish_datetime = datetime.now()
    req.save()
    data = {
    }
    return JsonResponse(data)

def rework_request(request):
    req_id = request.GET['req_id']
    req = Request.objects.get(id=req_id)
    req.status = 'On Progress'
    req.reason = None
    req.save()
    data = {
    }
    return JsonResponse(data)

def manage_member(request):
    req_id = request.GET['req_id']
    username_list = request.GET.getlist('username_list[]')
    req = Request.objects.get(id=req_id)
    members = Member.objects.filter(req=req)
    members.delete()
    for username in username_list:
        user = User.objects.get(username=username)
        member_new = Member(req=req,user=user)
        member_new.save()
    data = {
    }
    return JsonResponse(data)

def manage_vendor(request):
    req_id = request.GET['req_id']
    ven_code_list = request.GET.getlist('ven_code_list[]')
    req = Request.objects.get(id=req_id)
    req_vens = RequestVendor.objects.filter(req=req)
    req_vens.delete()
    for ven_code in ven_code_list:
        ven = Vendor.objects.get(code=ven_code)
        req_ven_new = RequestVendor(req=req,ven=ven)
        req_ven_new.save()
    data = {
    }
    return JsonResponse(data)

def manage_category(request):
    req_id = request.GET['req_id']
    sub_cat_id_list = request.GET.getlist('sub_cat_id_list[]')
    req = Request.objects.get(id=req_id)
    req_sub_cats = RequestSubCategory.objects.filter(req=req)
    req_sub_cats.delete()
    for sub_cat_id in sub_cat_id_list:
        sub_cat = SubCategory.objects.get(id=sub_cat_id)
        req_sub_cat_new = RequestSubCategory(req=req,sub_cat=sub_cat)
        req_sub_cat_new.save()
    data = {
    }
    return JsonResponse(data)

def post_comment(request):
    req_id = request.GET['req_id']
    comment_text = request.GET['comment_text']
    req = Request.objects.get(id=req_id)
    comment_new = Comment(req=req,text=comment_text,user=request.user)
    comment_new.save()
    data = {
    }
    return JsonResponse(data)

def delete_comment(request):
    comment_id = request.GET['comment_id']
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    data = {
    }
    return JsonResponse(data)

def owt_save(request):
    req_id = request.GET['req_id']
    username_list = request.GET.getlist('username_list[]')
    start_datetime = request.GET['start_datetime']
    stop_datetime = request.GET['stop_datetime']
    req = Request.objects.get(id=req_id)
    for username in username_list:
        user = User.objects.get(username=username)
        owt_new = OperatorWorkingTime(req=req,user=user,start_datetime=start_datetime,stop_datetime=stop_datetime)
        owt_new.save()
    data = {
    }
    return JsonResponse(data)

def delete_owt(request):
    owt_id = request.GET['owt_id']
    owt = OperatorWorkingTime.objects.get(id=owt_id)
    owt.delete()
    data = {
    }
    return JsonResponse(data)

def vwt_save(request):
    req_id = request.GET['req_id']
    ven_code_list = request.GET.getlist('ven_code_list[]')
    start_datetime = request.GET['start_datetime']
    stop_datetime = request.GET['stop_datetime']
    req = Request.objects.get(id=req_id)
    for ven_code in ven_code_list:
        ven = Vendor.objects.get(code=ven_code)
        owt_new = VendorWorkingTime(req=req,ven=ven,start_datetime=start_datetime,stop_datetime=stop_datetime)
        owt_new.save()
    data = {
    }
    return JsonResponse(data)

def delete_vwt(request):
    vwt_id = request.GET['vwt_id']
    vwt = VendorWorkingTime.objects.get(id=vwt_id)
    vwt.delete()
    data = {
    }
    return JsonResponse(data)

def mcdt_save(request):
    req_id = request.GET['req_id']
    mc_no = request.GET['mc_no']
    start_datetime = request.GET['start_datetime']
    stop_datetime = request.GET['stop_datetime']
    req = Request.objects.get(id=req_id)
    mc = Machine.objects.get(mc_no=mc_no)
    mcdt_new = MachineDowntime(req=req,mc=mc,start_datetime=start_datetime,stop_datetime=stop_datetime)
    mcdt_new.save()
    data = {
    }
    return JsonResponse(data)

def delete_mcdt(request):
    mcdt_id = request.GET['mcdt_id']
    mcdt = MachineDowntime.objects.get(id=mcdt_id)
    mcdt.delete()
    data = {
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
        mc_no = ws['A' + str(i)].value
        section = ws['B' + str(i)].value
        register_no = ws['C' + str(i)].value
        asset_no = ws['D' + str(i)].value
        serial_no = ws['E' + str(i)].value
        manufacture = ws['F' + str(i)].value
        model = ws['G' + str(i)].value
        plant = ws['H' + str(i)].value
        power  = ws['I' + str(i)].value
        install_date = ws['J' + str(i)].value
        capacity = ws['K' + str(i)].value
        note = ws['L' + str(i)].value
        if mc_no != None and mc_no != "":
            print(mc_no)
            mc_new = Machine(mc_no=mc_no,section=section,register_no=register_no,asset_no=asset_no,serial_no=serial_no,manufacture=manufacture,model=model,plant=plant,power=power,install_date=install_date,capacity=capacity,note=note)
            mc_new.save()
    return

def upload_task():
    entries = Task.objects.all()
    entries.delete()
    wb = load_workbook(filename = 'media/CMS Task Master.xlsx')
    ws = wb.active
    skip_count = 2
    for i in range(ws.max_row + 1):
        if i < skip_count:
            continue
        name = (ws['A' + str(i)].value).strip()
        type = (ws['B' + str(i)].value).strip()
        note = ws['C' + str(i)].value
        if name != None and name != "":
            print(type, name)
            task_new = Task(name=name,type=type,note=note)
            task_new.save()
    return

def upload_vendor():
    entries = Vendor.objects.all()
    entries.delete()
    wb = load_workbook(filename = 'media/CMS Vendor Master.xlsx')
    ws = wb.active
    skip_count = 2
    for i in range(ws.max_row + 1):
        if i < skip_count:
            continue
        code = ws['A' + str(i)].value
        name = (ws['B' + str(i)].value).strip()
        email = ws['C' + str(i)].value
        phone_no = ws['D' + str(i)].value
        note = ws['F' + str(i)].value
        if code != None and code != "":
            print(code, name)
            ven_new = Vendor(code=code,name=name,email=email,phone_no=phone_no,note=note)
            ven_new.save()
    return

################################ Other Function ################################

def create_req_no(id):
    req_no = str(id)
    for i in range(7 - len(str(id))):
        req_no = "0" + req_no
    req_no = "CMS" + req_no
    return req_no

def sort_user_by_section(users):
    f_users = []
    emps = Employee.objects.filter(user__in=users).order_by('section')
    for emp in emps:
        f_users.append(emp.user)
    return f_users

def get_mc_group(mcs):
    mc_group = []
    temp = ""
    for mc in mcs:
        if temp != mc.section:
            temp = mc.section
            mc_group.append(mc.section)
        else:
            mc_group.append(None)
    return mc_group

def get_task_group(tasks):
    task_group = []
    temp = ""
    for task in tasks:
        if temp != task.type:
            temp = task.type
            task_group.append(task.type)
        else:
            task_group.append(None)
    return task_group

def get_user_group(users):
    user_group = []
    temp = ""
    for user in users:
        if temp != user.employee.section:
            temp = user.employee.section
            user_group.append(user.employee.section)
        else:
            user_group.append(None)
    return user_group

def get_sub_cat_group(sub_cats):
    sub_cat_group = []
    temp = ""
    for sub_cat in sub_cats:
        if temp != sub_cat.cat.name:
            temp = sub_cat.cat.name
            sub_cat_group.append(sub_cat.cat.name)
        else:
            sub_cat_group.append(None)
    return sub_cat_group

def get_req_sub_cat_group(req_sub_cats):
    req_sub_cat_group = []
    temp = ""
    for req_sub_cat in req_sub_cats:
        if temp != req_sub_cat.sub_cat.cat.name:
            temp = req_sub_cat.sub_cat.cat.name
            req_sub_cat_group.append(req_sub_cat.sub_cat.cat.name)
        else:
            req_sub_cat_group.append(None)
    return req_sub_cat_group

def get_is_members(reqs, request):
    is_members = []
    for req in reqs:
        is_member = Member.objects.filter(req=req,user=request.user).exists()
        if is_member:
            is_members.append(True)
        else:
            is_members.append(False)
    return is_members

def get_select_members(req, users):
    select_members = []
    for user in users:
        is_member_exist = Member.objects.filter(req=req,user=user).exists()
        if is_member_exist:
            select_members.append(True)
        else:
            select_members.append(False)
    return select_members

def get_select_vendors(req, vens):
    select_vendors = []
    for ven in vens:
        is_ven_exist = RequestVendor.objects.filter(req=req,ven=ven).exists()
        if is_ven_exist:
            select_vendors.append(True)
        else:
            select_vendors.append(False)
    return select_vendors

def get_select_sub_cats(req, sub_cats):
    select_sub_cats = []
    for sub_cat in sub_cats:
        is_sub_cat_exist = RequestSubCategory.objects.filter(req=req,sub_cat=sub_cat).exists()
        if is_sub_cat_exist:
            select_sub_cats.append(True)
        else:
            select_sub_cats.append(False)
    return select_sub_cats

def is_in_section_group(request):
    sgs = SectionGroup.objects.all()
    is_in = False
    for sg in sgs:
        if sg.name == request.user.employee.section:
            is_in = True
    return is_in

def get_mail_group(sg, is_cc):
    list = []
    mgs = MailGroup.objects.filter(sg=sg,is_cc=is_cc)
    for mg in mgs:
        list.append(mg.user.email)
    return list

##################################### Email ####################################

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

def send_email(subject, email_content, send_to, cc_to):
    try:
        email = EmailMessage(subject, email_content, EMAIL_HOST_USER, send_to, cc_to)
        email.content_subtype = "html"
        EmailThread(email).start()
    except Exception:
        traceback.print_exc()
    return
