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
# Date Time
from datetime import datetime, timedelta

from .models import Employee, Machine,  Category, Request, File, Member, Comment, RequestCategory, OperatorWorkingTime

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
        return redirect('/index/')
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
    requestIsExist = Request.objects.filter(req_no=request_no).exists()
    req = None
    isJoined = False
    members = []
    comments = []
    reqcats = []
    files = []
    owts = []
    users = []
    cats = []
    if requestIsExist:
        req = Request.objects.get(req_no=request_no)
        isJoined = Member.objects.filter(req=req,user=request.user).exists()
        members = Member.objects.filter(req=req)
        comments = Comment.objects.filter(req=req).order_by('-date_published')
        reqcats = RequestCategory.objects.filter(req=req)
        files = File.objects.filter(req=req)
        owts = OperatorWorkingTime.objects.filter(req=req).order_by('-start_datetime')
        temp_users = User.objects.filter(is_active=True)
        for user in temp_users:
            if user.employee.section == req.req_to:
                users.append(user)
        cats = Category.objects.all()
    context = {
        'request_no': request_no,
        'requestIsExist': requestIsExist,
        'req': req,
        'isJoined': isJoined,
        'members': members,
        'comments': comments,
        'reqcats': reqcats,
        'files': files,
        'owts': owts,
        'users': users,
        'cats': cats,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_page.html', context)

#------------------------------------ Main ------------------------------------#

def all_page_data(request):
    my_reqs = []
    temp_reqs = Request.objects.filter(status='On Progress') | Request.objects.filter(status='On Hold')
    for req in temp_reqs:
        isMember = Member.objects.filter(req=req,user=request.user).exists()
        if isMember:
            my_reqs.append(req)
    my_request_count = len(my_reqs)
    pending_reqs = []
    if request.user.employee.view_type != 'ALL':
        pending_reqs = Request.objects.filter(status='Pending',req_to=request.user.employee.view_type)
    else:
        pending_reqs = Request.objects.filter(status='Pending')
    pending_request_count = len(pending_reqs)
    all_request_count = len(temp_reqs)
    context = {
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
        isMember = Member.objects.filter(req=req,user=request.user).exists()
        if isMember:
            reqs.append(req)
    context = {
        'reqs': reqs,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'index.html', context)

@login_required(login_url='/')
def request_pending(request):
    reqs = []
    if request.user.employee.view_type != 'ALL':
        reqs = Request.objects.filter(status='Pending',req_to=request.user.employee.view_type)
    else:
        reqs = Request.objects.filter(status='Pending')
    context = {
        'reqs': reqs,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_pending.html', context)

@login_required(login_url='/')
def request_all(request):
    reqs = []
    if request.user.employee.view_type != 'ALL':
        reqs = Request.objects.filter(status='On Progress',req_to=request.user.employee.view_type) | Request.objects.filter(status='On Hold',req_to=request.user.employee.view_type)
    else:
        reqs = Request.objects.filter(status='On Progress')  | Request.objects.filter(status='On Hold')
    joinings = []
    for req in reqs:
        isMember = Member.objects.filter(req=req,user=request.user).exists()
        if isMember:
            joinings.append('YES')
        else:
            joinings.append('NO')
    context = {
        'reqs': reqs,
        'joinings': joinings,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_all.html', context)

@login_required(login_url='/')
def request_history(request, fstartdate, fstopdate):
    if fstartdate == "NOW":
        fstartdate = datetime.today().strftime('%Y-%m-%d')
    if fstopdate == "NOW":
        fstopdate = datetime.today().strftime('%Y-%m-%d')
    reqs = []
    if request.user.employee.view_type != 'ALL':
        reqs = Request.objects.filter(status='Rejected',req_to=request.user.employee.view_type) | Request.objects.filter(status='Complete',req_to=request.user.employee.view_type) | Request.objects.filter(status='Canceled',req_to=request.user.employee.view_type)
    else:
        reqs = Request.objects.filter(status='Rejected')  | Request.objects.filter(status='Complete') | Request.objects.filter(status='Canceled')
    joinings = []
    for req in reqs:
        isMember = Member.objects.filter(req=req,user=request.user).exists()
        if isMember:
            joinings.append('YES')
        else:
            joinings.append('NO')
    context = {
        'fstartdate': fstartdate,
        'fstopdate': fstopdate,
        'reqs': reqs,
        'joinings': joinings,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_history.html', context)

#----------------------------------- Master -----------------------------------#

@login_required(login_url='/')
def master_emp(request):
    users = []
    temp_users = User.objects.all()
    if request.user.employee.view_type != 'ALL':
        for user in temp_users:
            if user.employee.view_type == request.user.employee.view_type:
                users.append(user)
    else:
        users = temp_users
    context = {
        'users': users,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'master_emp.html', context)

@login_required(login_url='/')
def master_mc(request):
    mcs = []
    temp_mcs = Machine.objects.all()
    if request.user.employee.view_type != 'ALL':
        for mc in temp_mcs:
            if mc.mc_of == request.user.employee.view_type:
                mcs.append(mc)
    else:
        mcs = temp_mcs
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
    cats = Category.objects.all()
    context = {
        'cats': cats,
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

#################################### POST ######################################
def new_request_save(request):
    emp_id = request.POST['emp_id']
    name = request.POST['name']
    section = request.POST['section']
    phone_no = request.POST['phone_no']
    req_to = request.POST['req_to']
    ma_mc_no = request.POST['ma_mc_no']
    ad_ser_mc_no = request.POST['ad_ser_mc_no']
    description = request.POST['description']
    type = 'Breakdown'
    status = 'Pending'
    request_date = datetime.now().date()
    mc_no = ma_mc_no if req_to == 'MA' else ad_ser_mc_no
    mc = None
    if mc_no != "Select":
        mc = Machine.objects.get(mc_no=mc_no)
    request_new = Request(emp_id=emp_id,name=name,section=section,phone_no=phone_no,req_to=req_to,type=type,status=status,request_date=request_date,mc=mc,description=description)
    request_new.save()
    request_new.req_no = create_req_no(request_new.id)
    request_new.save()
    return redirect('/')

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

##################################### GET ######################################

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

def find_emp_info(request):
    emp_id = request.GET['emp_id']
    found = False
    name = ""
    section = ""
    phone_no = ""
    reqs = Request.objects.filter(emp_id=emp_id).order_by('-date_published')
    if reqs:
        found = True
        name = reqs[0].name
        section = reqs[0].section
        phone_no = reqs[0].phone_no
    data = {
        'found': found,
        'name': name,
        'section': section,
        'phone_no': phone_no,
    }
    return JsonResponse(data)

def accept_request(request):
    req_id = request.GET['req_id']
    username_list = request.GET.getlist('username_list[]')
    cat_id_list = request.GET.getlist('cat_id_list[]')
    req = Request.objects.get(id=req_id)
    for username in username_list:
        user = User.objects.get(username=username)
        member_new = Member(req=req,user=user)
        member_new.save()
    for cat_id in cat_id_list:
        cat = Category.objects.get(id=cat_id)
        reqcat_new = RequestCategory(req=req,cat=cat)
        reqcat_new.save()
    req.status = 'On Progress'
    req.save()
    data = {
    }
    return JsonResponse(data)

def reject_request(request):
    req_id = request.GET['req_id']
    is_nms = True if request.GET['is_nms'] == 'true' else False
    reject_reason = request.GET['reject_reason']
    req = Request.objects.get(id=req_id)
    if is_nms:
        req.req_to = 'MA' if req.req_to == 'AD-SER' else 'AD-SER'
        req.mc = None
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

def post_comment(request):
    req_id = request.GET['req_id']
    comment_text = request.GET['comment_text']
    req = Request.objects.get(id=req_id)
    comment_new = Comment(req=req,text=comment_text,user=request.user)
    comment_new.save()
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

################################ Other Function ################################

def create_req_no(id):
    req_no = str(id)
    for i in range(6 - len(str(id))):
        req_no = "0" + req_no
    req_no = "CMS" + req_no
    return req_no
