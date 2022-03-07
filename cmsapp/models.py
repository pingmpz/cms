from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=10)
    view_type = models.CharField(max_length=10)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Machine(models.Model):
    mc_no = models.CharField(max_length=50, primary_key=True)
    mc_of = models.CharField(max_length=10)
    section = models.CharField(max_length=50, null=True)
    register_no = models.CharField(max_length=50, null=True)
    asset_no = models.CharField(max_length=50, null=True)
    serial_no = models.CharField(max_length=50, null=True)
    manufacture = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=50, null=True)
    plant = models.CharField(max_length=10, null=True)
    power = models.CharField(max_length=50, null=True)
    install_date = models.DateField(null=True)
    capacity = models.CharField(max_length=1000, null=True)
    note = models.CharField(max_length=1000, null=True)
    is_active = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    cat_of = models.CharField(max_length=10)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    req_no = models.CharField(max_length=10)
    emp_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=10)
    req_to = models.CharField(max_length=10)
    mc = models.ForeignKey(Machine, null=True, on_delete=models.SET_NULL)
    request_date = models.DateField(null=True)
    finish_datetime = models.DateTimeField(null=True)
    type = models.CharField(max_length=10) # Preventive, Breakdown
    status = models.CharField(max_length=20) # Pending, Rejected, On Progress, On Hold, Complete, Canceled
    reason = models.CharField(max_length=1000, null=True)
    description = models.CharField(max_length=1000)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

class File(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=1000, null=True)
    date_published = models.DateTimeField(auto_now_add=True)

class RequestCategory(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)

class OperatorWorkingTime(models.Model):
    id = models.AutoField(primary_key=True)
    req = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
