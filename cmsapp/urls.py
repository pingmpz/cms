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
    path('new_request/<str:sg_name>', views.new_request, name='new_request'),
    path('new_request_success/<str:request_no>', views.new_request_success, name='new_request_success'),
    path('new_pv_request/', views.new_pv_request, name='new_pv_request'),
    path('new_pv_request_ma/', views.new_pv_request_ma, name='new_pv_request_ma'),
    path('request_page/<str:request_no>', views.request_page, name='request_page'),
    path('req/<str:request_id>', views.req, name='req'),
    path('edit_request/<str:request_no>', views.edit_request, name='edit_request'),
    #--
    path('index/', views.index, name='index'),
    path('request_pending/<str:fsg>', views.request_pending, name='request_pending'),
    path('request_pv_pending/<str:fsg>', views.request_pv_pending, name='request_pv_pending'),
    path('request_all/<str:fsg>&<str:fstatus>&<str:ftype>', views.request_all, name='request_all'),
    path('request_breakdown/<str:fsg>', views.request_breakdown, name='request_breakdown'),
    path('request_history/<str:fsg>&<str:fstatus>&<str:ftype>&<str:fstartdate>&<str:fstopdate>', views.request_history, name='request_history'),
    path('cri_part_list/', views.cri_part_list, name='cri_part_list'),
    path('spl_part_list/', views.spl_part_list, name='spl_part_list'),
    path('pwst_list/', views.pwst_list, name='pwst_list'),
    path('mc_page/<str:mc_no>', views.mc_page, name='mc_page'),
    #-- Report
    path('report/summary/<str:fsg>', views.summary, name='summary'),
    path('report/pv_calendar/<str:fmcg>&<str:fyear>', views.pv_calendar, name='pv_calendar'),
    path('report/q_obj/<str:fmcg>&<str:fyear>', views.report_q_obj, name='report_q_obj'),
    path('report/working_time/<str:fuser>&<str:fstartdate>&<str:fstopdate>', views.working_time, name='working_time'),
    path('report/mc_dt/<str:fsection>&<str:fmonth>', views.report_mc_dt, name='report_mc_dt'),
    path('report/cat/<str:fsc>', views.report_cat, name='report_cat'),
    #-- Master
    path('master/emp/', views.master_emp, name='master_emp'),
    path('master/mcg/', views.master_mcg, name='master_mcg'),
    path('master/mc/', views.master_mc, name='master_mc'),
    path('master/task/', views.master_task, name='master_task'),
    path('master/ven/', views.master_ven, name='master_ven'),
    path('master/cat/', views.master_cat, name='master_cat'),
    path('master/sub_cat/', views.master_sub_cat, name='master_sub_cat'),
    path('master/sg/', views.master_sg, name='master_sg'),
    path('master/mg/', views.master_mg, name='master_mg'),
    #-- New Data
    path('new/emp/', views.new_emp, name='new_emp'),
    path('new/mc/', views.new_mc, name='new_mc'),
    path('new/cp/', views.new_cp, name='new_cp'),
    path('new/sp/', views.new_sp, name='new_sp'),
    path('new/task/', views.new_task, name='new_task'),
    path('new/ven/', views.new_ven, name='new_ven'),
    path('new/cat/', views.new_cat, name='new_cat'),
    path('new/sub_cat/', views.new_sub_cat, name='new_sub_cat'),
    path('new/mg/', views.new_mg, name='new_mg'),
    path('new/pwst/', views.new_pwst, name='new_pwst'),
    #-- Edit Data
    path('edit/mc/<str:fmc>', views.edit_mc, name='edit_mc'),
    path('edit/cp/<str:fcp>', views.edit_cp, name='edit_cp'),
    path('edit/sp/<str:fsp>', views.edit_sp, name='edit_sp'),
    path('edit/task/<str:ftask>', views.edit_task, name='edit_task'),
    path('edit/ven/<str:fven>', views.edit_ven, name='edit_ven'),
    path('edit/pwst/<str:fpwst>', views.edit_pwst, name='edit_pwst'),
    ### POST
    path('setting_save/', views.setting_save, name='setting_save'),
    path('new_request_save/', views.new_request_save, name='new_request_save'),
    path('new_pv_request_save/', views.new_pv_request_save, name='new_pv_request_save'),
    path('new_pv_request_ma_save/', views.new_pv_request_ma_save, name='new_pv_request_ma_save'),
    path('edit_request_save/', views.edit_request_save, name='edit_request_save'),
    #-- New Data
    path('new_emp_save/', views.new_emp_save, name='new_emp_save'),
    path('new_mc_save/', views.new_mc_save, name='new_mc_save'),
    path('new_cp_save/', views.new_cp_save, name='new_cp_save'),
    path('new_sp_save/', views.new_sp_save, name='new_sp_save'),
    path('new_task_save/', views.new_task_save, name='new_task_save'),
    path('new_ven_save/', views.new_ven_save, name='new_ven_save'),
    path('new_cat_save/', views.new_cat_save, name='new_cat_save'),
    path('new_sub_cat_save/', views.new_sub_cat_save, name='new_sub_cat_save'),
    path('new_mg_save/', views.new_mg_save, name='new_mg_save'),
    path('new_pwst_save/', views.new_pwst_save, name='new_pwst_save'),
    #-- Edit Data
    path('edit_mc_save/', views.edit_mc_save, name='edit_mc_save'),
    path('edit_cp_save/', views.edit_cp_save, name='edit_cp_save'),
    path('edit_sp_save/', views.edit_sp_save, name='edit_sp_save'),
    path('edit_task_save/', views.edit_task_save, name='edit_task_save'),
    path('edit_ven_save/', views.edit_ven_save, name='edit_ven_save'),
    path('edit_pwst_save/', views.edit_pwst_save, name='edit_pwst_save'),
    ### GET
    path('validate_old_password/', views.validate_old_password, name='validate_old_password'),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('validate_mc_no/', views.validate_mc_no, name='validate_mc_no'),
    path('validate_cp/', views.validate_cp, name='validate_cp'),
    path('validate_task/', views.validate_task, name='validate_task'),
    path('validate_vendor_code/', views.validate_vendor_code, name='validate_vendor_code'),
    path('validate_category_name/', views.validate_category_name, name='validate_category_name'),
    path('validate_sub_category_name/', views.validate_sub_category_name, name='validate_sub_category_name'),
    path('validate_user_in_mail_group/', views.validate_user_in_mail_group, name='validate_user_in_mail_group'),
    path('validate_pwst/', views.validate_pwst, name='validate_pwst'),
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
    path('set_breakdown/', views.set_breakdown, name='set_breakdown'),
    path('remove_breakdown/', views.remove_breakdown, name='remove_breakdown'),
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
    path('cost_save/', views.cost_save, name='cost_save'),
    path('delete_cost/', views.delete_cost, name='delete_cost'),
    path('set_tot/', views.set_tot, name='set_tot'),
    path('set_ewt/', views.set_ewt, name='set_ewt'),
    path('set_target/', views.set_target, name='set_target'),
    #-- File
    path('file_save/', views.file_save, name='file_save'),
    #-- API
    path('api/get_emp_work_time/<str:emp_id>&<str:start_date>&<str:end_date>', views.api_get_emp_work_time, name='api_get_emp_work_time'),
    #-- ETC
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
]+ static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)
