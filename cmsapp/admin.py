from django.contrib import admin
from .models import Employee, Machine, Category, Request, File, Member, Comment, RequestCategory, OperatorWorkingTime

admin.site.register(Employee)
admin.site.register(Machine)
admin.site.register(Category)
admin.site.register(Request)
admin.site.register(File)
admin.site.register(Member)
admin.site.register(Comment)
admin.site.register(RequestCategory)
admin.site.register(OperatorWorkingTime)
