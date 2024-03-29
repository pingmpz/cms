from django.contrib import admin
from .models import SectionGroup, Employee, MachineGroup, Machine, Task, Vendor, Category, SubCategory, MailGroup, CriticalPart, SplindlePart, PasswordStorage, PasswordItem, Request, File, Member, RequestVendor, Comment, RequestSubCategory, OperatorWorkingTime, VendorWorkingTime, MachineDowntime, Costing, TotalOperationTime, QualityObjectiveTarget, EstimateWorkingTime

admin.site.register(SectionGroup)
admin.site.register(Employee)
admin.site.register(MachineGroup)
admin.site.register(Machine)
admin.site.register(Task)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(MailGroup)
admin.site.register(CriticalPart)
admin.site.register(SplindlePart)
admin.site.register(PasswordStorage)
admin.site.register(PasswordItem)
admin.site.register(Request)
admin.site.register(File)
admin.site.register(Member)
admin.site.register(RequestVendor)
admin.site.register(Comment)
admin.site.register(RequestSubCategory)
admin.site.register(OperatorWorkingTime)
admin.site.register(VendorWorkingTime)
admin.site.register(MachineDowntime)
admin.site.register(Costing)
admin.site.register(TotalOperationTime)
admin.site.register(QualityObjectiveTarget)
admin.site.register(EstimateWorkingTime)
