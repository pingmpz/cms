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

from .models import Employee, Machine, Category, SubCategory, SectionGroup, SectionGroupMember, Request, File, Member, Comment, RequestSubCategory, OperatorWorkingTime, MachineDowntime

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
    sgs = SectionGroup.objects.all()
    context = {
        'sgs': sgs,
    }
    return render(request, 'new_request.html', context)

def new_pv_request(request):
    sgs = SectionGroup.objects.all()
    mcs = Machine.objects.filter(is_active=True).order_by('section')
    mc_group = get_mc_group(mcs)
    context = {
        'sgs': sgs,
        'mcs': mcs,
        'mc_group': mc_group,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_pv_request.html', context)

@login_required(login_url='/')
def request_page(request, request_no):
    req_is_exist = Request.objects.filter(req_no=request_no).exists()
    req = None
    is_member = False
    members = [] # Member (User)
    comments = [] # Comment
    req_sub_cats = [] # RequestSubCategory
    req_sub_cat_group = [] # RequestSubCategory Group (Category)
    files = [] # Files
    owts = [] # OpereatorWorkTime
    mcdts = [] # MachineDowntime

    sgs = [] # All Available SectionGroup
    mcs = [] # All Available Machine
    users = [] # All Available User
    sub_cats = [] # All Available SubCategory

    mc_group = [] # Machine Group (Section)
    user_group = [] # User Group (Section)
    sub_cat_group = [] # SubCategory Group (Category)

    select_members = [] # For Manage Member
    select_sub_cats = [] # For Manage Category
    if req_is_exist:
        req = Request.objects.get(req_no=request_no)
        is_member = Member.objects.filter(req=req,user=request.user).exists()
        members = Member.objects.filter(req=req)
        comments = Comment.objects.filter(req=req).order_by('-date_published')
        req_sub_cats = RequestSubCategory.objects.filter(req=req)
        req_sub_cat_group = get_req_sub_cat_group(req_sub_cats)
        files = File.objects.filter(req=req)
        owts = OperatorWorkingTime.objects.filter(req=req).order_by('-start_datetime')
        mcdts = MachineDowntime.objects.filter(req=req).order_by('-start_datetime')
        sgs = SectionGroup.objects.all()
        mcs = Machine.objects.filter(is_active=True).order_by('section')
        users = sort_user_by_section(User.objects.filter(is_active=True))
        sub_cats = SubCategory.objects.all().order_by('cat')
        mc_group = get_mc_group(mcs)
        user_group = get_user_group(users)
        sub_cat_group = get_sub_cat_group(sub_cats)
        select_members = get_select_members(req, users)
        select_sub_cats = get_select_sub_cats(req, sub_cats)
    context = {
        'request_no': request_no,
        'req_is_exist': req_is_exist,
        'req': req,
        'is_member': is_member,
        'members': members,
        'comments': comments,
        'req_sub_cats': req_sub_cats,
        'req_sub_cat_group': req_sub_cat_group,
        'files': files,
        'owts': owts,
        'mcdts': mcdts,
        'sgs': sgs,
        'mcs': mcs,
        'users': users,
        'sub_cats': sub_cats,
        'mc_group': mc_group,
        'user_group': user_group,
        'sub_cat_group': sub_cat_group,
        'select_members': select_members,
        'select_sub_cats': select_sub_cats,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_page.html', context)

#------------------------------------ Main ------------------------------------#

def all_page_data(request):
    my_reqs = []
    temp_reqs = Request.objects.filter(status='On Progress') | Request.objects.filter(status='On Hold')
    for req in temp_reqs:
        is_member = Member.objects.filter(req=req,user=request.user).exists()
        if is_member:
            my_reqs.append(req)
    my_request_count = len(my_reqs)

    pending_reqs = Request.objects.filter(status='Pending')
    pending_request_count = len(pending_reqs)

    all_reqs = Request.objects.filter(status='On Progress')  | Request.objects.filter(status='On Hold')
    all_request_count = len(all_reqs)
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
        is_member = Member.objects.filter(req=req,user=request.user).exists()
        if is_member:
            reqs.append(req)
    context = {
        'reqs': reqs,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'index.html', context)

@login_required(login_url='/')
def request_pending(request):
    reqs = Request.objects.filter(status='Pending')
    context = {
        'reqs': reqs,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_pending.html', context)

@login_required(login_url='/')
def request_all(request):
    reqs = Request.objects.filter(status='On Progress')  | Request.objects.filter(status='On Hold')
    is_members = get_is_members(reqs, request)
    context = {
        'reqs': reqs,
        'is_members': is_members,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'request_all.html', context)

@login_required(login_url='/')
def request_history(request, fstartdate, fstopdate):
    if fstartdate == "NOW":
        fstartdate = datetime.today().strftime('%Y-%m-%d')
    if fstopdate == "NOW":
        fstopdate = datetime.today().strftime('%Y-%m-%d')
    reqs = Request.objects.filter(status='Rejected',finish_datetime__date__range=[fstartdate, fstopdate])  | Request.objects.filter(status='Complete',finish_datetime__date__range=[fstartdate, fstopdate]) | Request.objects.filter(status='Canceled',finish_datetime__date__range=[fstartdate, fstopdate])
    is_members = get_is_members(reqs, request)
    context = {
        'fstartdate': fstartdate,
        'fstopdate': fstopdate,
        'reqs': reqs,
        'is_members': is_members,
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

@login_required(login_url='/')
def new_sub_cat(request):
    cats = Category.objects.all()
    context = {
        'cats': cats,
    }
    context['all_page_data'] = (all_page_data(request))
    return render(request, 'new_sub_cat.html', context)

#################################### POST ######################################
def new_request_save(request):
    emp_id = request.POST['emp_id']
    name = request.POST['name']
    section = request.POST['section']
    phone_no = request.POST['phone_no']
    sg_name = request.POST['sg_name']
    description = request.POST['description']
    type = 'User Request'
    status = 'Pending'
    request_date = datetime.now().date()
    sg = SectionGroup.objects.get(name=sg_name)
    request_new = Request(emp_id=emp_id,name=name,section=section,phone_no=phone_no,sg=sg,type=type,status=status,request_date=request_date,description=description)
    request_new.save()
    request_new.req_no = create_req_no(request_new.id)
    request_new.save()
    return redirect('/')

def new_pv_request_save(request):
    sg_name = request.POST['sg_name']
    request_date = request.POST['req_date']
    description = request.POST['description']
    mc_no = request.POST['mc_no'] if request.POST['mc_no'] != 'Select' else None
    mc = None
    if mc_no != None:
        mc = Machine.objects.get(mc_no=mc_no)
    type = 'Preventive'
    status = 'Pending'
    sg = SectionGroup.objects.get(name=sg_name)
    emp_id = request.user.username
    name = request.user.employee.name
    section = request.user.employee.section
    phone_no = request.user.employee.phone_no
    request_new = Request(emp_id=emp_id,name=name,section=section,phone_no=phone_no,sg=sg,type=type,status=status,request_date=request_date,description=description,mc=mc)
    request_new.save()
    request_new.req_no = create_req_no(request_new.id)
    request_new.save()
    return redirect('/new_pv_request/')

def new_emp_save(request):
    username = request.POST['new_username']
    password = request.POST['new_password']
    name = request.POST['name']
    section = request.POST['section']
    phone_no = request.POST['phone_no']
    user_new = User.objects.create_user(username, '', password)
    user_new.save()
    employee_new = Employee(user=user_new,name=name,section=section,phone_no=phone_no)
    employee_new.save()
    return redirect('/new_emp/')

def new_cat_save(request):
    name = request.POST['name']
    cat_new = Category(name=name)
    cat_new.save()
    return redirect('/new_cat/')

def new_sub_cat_save(request):
    name = request.POST['name']
    cat_id = request.POST['cat_id']
    description = request.POST['description']
    cat = Category.objects.get(id=cat_id)
    sub_cat_new = SubCategory(name=name,cat=cat,description=description)
    sub_cat_new.save()
    return redirect('/new_sub_cat/')

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

def validate_category_name(request):
    name = request.GET['name']
    canUse = True
    isExist = Category.objects.filter(name=name).exists()
    if isExist:
        canUse = False
    data = {
        'canUse': canUse,
    }
    return JsonResponse(data)

def validate_sub_category_name(request):
    name = request.GET['name']
    cat_id = request.GET['cat_id']
    canUse = True
    cat = Category.objects.get(id=cat_id)
    isExist = SubCategory.objects.filter(name=name,cat=cat).exists()
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
    mc_no = request.GET['mc_no'] if request.GET['mc_no'] != 'Select' else None
    username_list = request.GET.getlist('username_list[]')
    sub_cat_id_list = request.GET.getlist('sub_cat_id_list[]')
    req = Request.objects.get(id=req_id)
    if mc_no != None:
        mc = Machine.objects.get(mc_no=mc_no)
        req.mc = mc
    for username in username_list:
        user = User.objects.get(username=username)
        member_new = Member(req=req,user=user)
        member_new.save()
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

def get_select_sub_cats(req, sub_cats):
    select_sub_cats = []
    for sub_cat in sub_cats:
        is_sub_cat_exist = RequestSubCategory.objects.filter(req=req,sub_cat=sub_cat).exists()
        if is_sub_cat_exist:
            select_sub_cats.append(True)
        else:
            select_sub_cats.append(False)
    return select_sub_cats
