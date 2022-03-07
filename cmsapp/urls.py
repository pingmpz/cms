from django.urls import path

from . import views

urlpatterns = [
    ### Authenticate
    path('', views.first_page, name='first_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('validate_login/', views.validate_login, name='validate_login'),
    path('login_action/', views.login_action, name='login_action'),
    path('logout_action/', views.logout_action, name='logout_action'),
    ### Page
    path('new_request/', views.new_request, name='new_request'),
    path('new_pv_request/', views.new_pv_request, name='new_pv_request'),
    path('request_page/<str:request_no>', views.request_page, name='request_page'),
    #--
    path('index/', views.index, name='index'),
    path('request_pending/<str:freq>', views.request_pending, name='request_pending'),
    path('request_all/<str:freq>', views.request_all, name='request_all'),
    path('request_history/<str:freq>&<str:fstatus>&<str:fstartdate>&<str:fstopdate>', views.request_history, name='request_history'),
    #-- Master
    path('master_emp/', views.master_emp, name='master_emp'),
    path('master_mc/', views.master_mc, name='master_mc'),
    path('master_vendor/', views.master_vendor, name='master_vendor'),
    path('master_cat/', views.master_cat, name='master_cat'),
    #-- New Data
    path('new_emp/', views.new_emp, name='new_emp'),
    path('new_mc/', views.new_mc, name='new_mc'),
    path('new_vendor/', views.new_vendor, name='new_vendor'),
    path('new_cat/', views.new_cat, name='new_cat'),
    ### POST
    path('new_request_save/', views.new_request_save, name='new_request_save'),
    path('new_emp_save/', views.new_emp_save, name='new_emp_save'),
    ### GET
    path('validate_username/', views.validate_username, name='validate_username'),
    path('find_emp_info/', views.find_emp_info, name='find_emp_info'),
    path('post_comment/', views.post_comment, name='post_comment'),
    path('join_request/', views.join_request, name='join_request'),
    path('leave_request/', views.leave_request, name='leave_request'),
]
