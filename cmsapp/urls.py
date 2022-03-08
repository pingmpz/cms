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
    path('request_pending/', views.request_pending, name='request_pending'),
    path('request_all/', views.request_all, name='request_all'),
    path('request_history/<str:fstartdate>&<str:fstopdate>', views.request_history, name='request_history'),
    #-- Master
    path('master_emp/', views.master_emp, name='master_emp'),
    path('master_mc/', views.master_mc, name='master_mc'),
    path('master_vendor/', views.master_vendor, name='master_vendor'),
    path('master_cat/', views.master_cat, name='master_cat'),
    path('master_sub_cat/', views.master_sub_cat, name='master_sub_cat'),
    #-- New Data
    path('new_emp/', views.new_emp, name='new_emp'),
    path('new_mc/', views.new_mc, name='new_mc'),
    path('new_vendor/', views.new_vendor, name='new_vendor'),
    path('new_cat/', views.new_cat, name='new_cat'),
    path('new_sub_cat/', views.new_sub_cat, name='new_sub_cat'),
    ### POST
    path('new_request_save/', views.new_request_save, name='new_request_save'),
    path('new_pv_request_save/', views.new_pv_request_save, name='new_pv_request_save'),
    path('new_emp_save/', views.new_emp_save, name='new_emp_save'),
    path('new_cat_save/', views.new_cat_save, name='new_cat_save'),
    path('new_sub_cat_save/', views.new_sub_cat_save, name='new_sub_cat_save'),
    ### GET
    path('validate_username/', views.validate_username, name='validate_username'),
    path('validate_category_name/', views.validate_category_name, name='validate_category_name'),
    path('validate_sub_category_name/', views.validate_sub_category_name, name='validate_sub_category_name'),
    path('find_emp_info/', views.find_emp_info, name='find_emp_info'),
    #-- Request Page
    path('accept_request/', views.accept_request, name='accept_request'),
    path('reject_request/', views.reject_request, name='reject_request'),
    path('join_request/', views.join_request, name='join_request'),
    path('leave_request/', views.leave_request, name='leave_request'),
    path('hold_request/', views.hold_request, name='hold_request'),
    path('start_work_request/', views.start_work_request, name='start_work_request'),
    path('complete_request/', views.complete_request, name='complete_request'),
    path('cancel_request/', views.cancel_request, name='cancel_request'),
    path('rework_request/', views.rework_request, name='rework_request'),
    path('manage_member/', views.manage_member, name='manage_member'),
    path('manage_category/', views.manage_category, name='manage_category'),
    path('post_comment/', views.post_comment, name='post_comment'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('owt_save/', views.owt_save, name='owt_save'),
    path('delete_owt/', views.delete_owt, name='delete_owt'),
    path('mcdt_save/', views.mcdt_save, name='mcdt_save'),
    path('delete_mcdt/', views.delete_mcdt, name='delete_mcdt'),
]
