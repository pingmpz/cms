from django.db import models
from django.contrib.auth.models import User

class SectionGroup(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    full_name = models.CharField(max_length=100, null=True)
    line_token = models.CharField(max_length=100, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=10)
    scheme = models.CharField(max_length=10, default="Light Mode") # Light Mode, Dark Mode
    sidebar = models.CharField(max_length=10, default="Scrollable") # Scrollable, Condensed
    pv_created = models.CharField(max_length=20, default="Request Page") # Request Page, New Preventive Request
    auto_add = models.BooleanField(default=True)
    default_owt = models.CharField(max_length=20, default="None") # None, Only Me, All Member
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class MachineGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Machine(models.Model):
    mc_no = models.CharField(max_length=50, primary_key=True)
    section = models.CharField(max_length=50, null=True)
    mcg = models.ForeignKey(MachineGroup, null=True, on_delete=models.SET_NULL)
    register_no = models.CharField(max_length=50, null=True)
    asset_no = models.CharField(max_length=50, null=True)
    serial_no = models.CharField(max_length=50, null=True)
    manufacture = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=50, null=True)
    plant = models.CharField(max_length=10, null=True)
    power = models.CharField(max_length=50, null=True)
    install_date = models.DateField(null=True)
    capacity = models.TextField(max_length=1000, null=True)
    note = models.TextField(max_length=1000, null=True)
    is_active = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50, null=True)
    note = models.TextField(max_length=1000, null=True)
    is_active = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Vendor(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=1000, null=True)
    email = models.CharField(max_length=100, null=True)
    phone_no = models.CharField(max_length=20, null=True)
    note = models.TextField(max_length=1000, null=True)
    is_active = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class MailGroup(models.Model):
    id = models.AutoField(primary_key=True)
    sg = models.ForeignKey(SectionGroup, on_delete=models.CASCADE)
    is_cc = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class CriticalPart(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mat_code = models.CharField(max_length=100, null=True)
    amount = models.IntegerField(default=0)
    minimum = models.IntegerField(default=0) # 0 = Not Defined
    note = models.TextField(max_length=1000, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class SplindlePart(models.Model):
    id = models.AutoField(primary_key=True)
    machine = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100, null=True)
    amount = models.IntegerField(default=0)
    register_date = models.DateField(null=True)
    marker = models.CharField(max_length=100, null=True)
    serial_no = models.CharField(max_length=100, null=True)
    nose = models.CharField(max_length=100, null=True)
    max_speed = models.CharField(max_length=100, null=True)
    drive_type = models.CharField(max_length=100, null=True)
    lubrication = models.CharField(max_length=100, null=True)
    condition = models.CharField(max_length=100, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    req_no = models.CharField(max_length=10)
    emp_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    email = models.CharField(max_length=20, null=True, default=None)
    phone_no = models.CharField(max_length=10)
    sg = models.ForeignKey(SectionGroup, null=True, on_delete=models.SET_NULL)
    mc = models.ForeignKey(Machine, null=True, on_delete=models.SET_NULL)
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)
    request_date = models.DateField(null=True)
    finish_datetime = models.DateTimeField(null=True)
    type = models.CharField(max_length=10) # Preventive, User Request
    status = models.CharField(max_length=20) # Pending, Rejected, On Progress, On Hold, Complete, Canceled
    reason = models.TextField(max_length=1000, null=True)
    description = models.TextField(max_length=1000)
    corrective_action = models.TextField(max_length=1000, null=True)
    cause = models.TextField(max_length=1000, null=True)
    spare_parts = models.TextField(max_length=1000, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class File(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    date_published = models.DateTimeField(auto_now_add=True)

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)

class RequestVendor(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    ven = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=1000, null=True)
    date_published = models.DateTimeField(auto_now_add=True)

class RequestSubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    sub_cat = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)

class OperatorWorkingTime(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(null=True)
    stop_datetime = models.DateTimeField(null=True)
    date_published = models.DateTimeField(auto_now_add=True)

class VendorWorkingTime(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    ven = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(null=True)
    stop_datetime = models.DateTimeField(null=True)
    date_published = models.DateTimeField(auto_now_add=True)

class MachineDowntime(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    mc = models.ForeignKey(Machine, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(null=True)
    stop_datetime = models.DateTimeField(null=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Costing(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    date_published = models.DateTimeField(auto_now_add=True)

class TotalOperationTime(models.Model):
    id = models.AutoField(primary_key=True)
    mcg = models.ForeignKey(MachineGroup, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    time = models.IntegerField()
    date_published = models.DateTimeField(auto_now_add=True)

class QualityObjectiveTarget(models.Model):
    id = models.AutoField(primary_key=True)
    mcg = models.ForeignKey(MachineGroup, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    type = models.CharField(max_length=4)
    time = models.IntegerField()
    date_published = models.DateTimeField(auto_now_add=True)
