from django.contrib import admin
from .models import Employee, Machine, Category, SubCategory, SectionGroup, Request, File, Member, Comment, RequestSubCategory, OperatorWorkingTime, MachineDowntime

admin.site.register(Employee)
admin.site.register(Machine)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SectionGroup)
admin.site.register(Request)
admin.site.register(File)
admin.site.register(Member)
admin.site.register(Comment)
admin.site.register(RequestSubCategory)
admin.site.register(OperatorWorkingTime)
admin.site.register(MachineDowntime)
