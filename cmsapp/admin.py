from django.contrib import admin
from .models import Employee, Machine, Request, File, Member, Comment

admin.site.register(Employee)
admin.site.register(Machine)
admin.site.register(Request)
admin.site.register(File)
admin.site.register(Member)
admin.site.register(Comment)
