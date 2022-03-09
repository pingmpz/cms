from django.contrib import admin
from .models import SectionGroup, Employee, Machine, Vendor, Category, SubCategory, Request, File, Member, RequestVendor, Comment, RequestSubCategory, OperatorWorkingTime, VendorWorkingTime, MachineDowntime

admin.site.register(SectionGroup)
admin.site.register(Employee)
admin.site.register(Machine)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Request)
admin.site.register(File)
admin.site.register(Member)
admin.site.register(RequestVendor)
admin.site.register(Comment)
admin.site.register(RequestSubCategory)
admin.site.register(OperatorWorkingTime)
admin.site.register(VendorWorkingTime)
admin.site.register(MachineDowntime)
