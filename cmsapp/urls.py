from django.urls import path,include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from . import views

urlpatterns = [
    ### Authenticate
    path('', views.first_page, name='first_page'),
    path('track_request/<str:search_text>', views.track_request, name='track_request'),
    path('login_page/', views.login_page, name='login_page'),
    path('validate_login/', views.validate_login, name='validate_login'),
    path('login_action/', views.login_action, name='login_action'),
    path('logout_action/', views.logout_action, name='logout_action'),
    path('setting/', views.setting, name='setting'),
    ### Page
    path('new_request/', views.new_request, name='new_request'),
    path('new_request_success/<str:request_no>', views.new_request_success, name='new_request_success'),
    path('new_pv_request/', views.new_pv_request, name='new_pv_request'),
    path('edit_request/<str:request_no>', views.edit_request, name='edit_request'),
    path('request_page/<str:request_no>', views.request_page, name='request_page'),
    path('req/<str:request_id>', views.req, name='req'),
    #--
    path('index/', views.index, name='index'),
    path('request_pending/<str:fsg>', views.request_pending, name='request_pending'),
    path('request_pv_pending/<str:fsg>', views.request_pv_pending, name='request_pv_pending'),
    path('request_all/<str:fsg>', views.request_all, name='request_all'),
    path('request_history/<str:fsg>&<str:fstatus>&<str:ftype>&<str:fstartdate>&<str:fstopdate>', views.request_history, name='request_history'),
    #-- Report
    path('summary/<str:fsg>', views.summary, name='summary'),
    path('q_obj/<str:fgroup>&<str:fyear>', views.q_obj, name='q_obj'),
    #-- Master
    path('master_emp/', views.master_emp, name='master_emp'),
    path('master_mc/', views.master_mc, name='master_mc'),
    path('master_task/', views.master_task, name='master_task'),
    path('master_ven/', views.master_ven, name='master_ven'),
    path('master_cat/', views.master_cat, name='master_cat'),
    path('master_sub_cat/', views.master_sub_cat, name='master_sub_cat'),
    path('master_sg/', views.master_sg, name='master_sg'),
    path('master_mg/', views.master_mg, name='master_mg'),
    #-- New Data
    path('new_emp/', views.new_emp, name='new_emp'),
    path('new_mc/', views.new_mc, name='new_mc'),
    path('new_task/', views.new_task, name='new_task'),
    path('new_ven/', views.new_ven, name='new_ven'),
    path('new_cat/', views.new_cat, name='new_cat'),
    path('new_sub_cat/', views.new_sub_cat, name='new_sub_cat'),
    path('new_mg/', views.new_mg, name='new_mg'),
    #-- Edit Data
    path('edit_mc/<str:fmc>', views.edit_mc, name='edit_mc'),
    path('edit_task/<str:ftask>', views.edit_task, name='edit_task'),
    path('edit_ven/<str:fven>', views.edit_ven, name='edit_ven'),
    ### POST
    path('setting_save/', views.setting_save, name='setting_save'),
    path('new_request_save/', views.new_request_save, name='new_request_save'),
    path('new_pv_request_save/', views.new_pv_request_save, name='new_pv_request_save'),
    path('edit_request_save/', views.edit_request_save, name='edit_request_save'),
    #-- New Data
    path('new_emp_save/', views.new_emp_save, name='new_emp_save'),
    path('new_mc_save/', views.new_mc_save, name='new_mc_save'),
    path('new_task_save/', views.new_task_save, name='new_task_save'),
    path('new_ven_save/', views.new_ven_save, name='new_ven_save'),
    path('new_cat_save/', views.new_cat_save, name='new_cat_save'),
    path('new_sub_cat_save/', views.new_sub_cat_save, name='new_sub_cat_save'),
    path('new_mg_save/', views.new_mg_save, name='new_mg_save'),
    #-- Edit Data
    path('edit_mc_save/', views.edit_mc_save, name='edit_mc_save'),
    path('edit_task_save/', views.edit_task_save, name='edit_task_save'),
    path('edit_ven_save/', views.edit_ven_save, name='edit_ven_save'),
    ### GET
    path('validate_old_password/', views.validate_old_password, name='validate_old_password'),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('validate_mc_no/', views.validate_mc_no, name='validate_mc_no'),
    path('validate_task/', views.validate_task, name='validate_task'),
    path('validate_vendor_code/', views.validate_vendor_code, name='validate_vendor_code'),
    path('validate_category_name/', views.validate_category_name, name='validate_category_name'),
    path('validate_sub_category_name/', views.validate_sub_category_name, name='validate_sub_category_name'),
    path('validate_user_in_mail_group/', views.validate_user_in_mail_group, name='validate_user_in_mail_group'),
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
    path('manage_vendor/', views.manage_vendor, name='manage_vendor'),
    path('manage_category/', views.manage_category, name='manage_category'),
    path('post_comment/', views.post_comment, name='post_comment'),
    path('delete_file/', views.delete_file, name='delete_file'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('owt_save/', views.owt_save, name='owt_save'),
    path('delete_owt/', views.delete_owt, name='delete_owt'),
    path('vwt_save/', views.vwt_save, name='vwt_save'),
    path('delete_vwt/', views.delete_vwt, name='delete_vwt'),
    path('mcdt_save/', views.mcdt_save, name='mcdt_save'),
    path('delete_mcdt/', views.delete_mcdt, name='delete_mcdt'),
    #-- File
    path('file_save/', views.file_save, name='file_save'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
]+ static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)
