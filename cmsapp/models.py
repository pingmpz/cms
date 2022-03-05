from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    view_type = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=10)
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
