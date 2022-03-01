from django.urls import path

from . import views

urlpatterns = [
    # Authenticate
    path('', views.first_page, name='first_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('validate_login/', views.validate_login, name='validate_login'),
    path('login_action/', views.login_action, name='login_action'),
    path('logout_action/', views.logout_action, name='logout_action'),
    path('new_request/', views.new_request, name='new_request'),
    path('index/', views.index, name='index'),
    path('index0/', views.index0, name='index0'),
    path('pending_request/', views.pending_request, name='pending_request'),
    path('history_request/', views.history_request, name='history_request'),
    path('emp_master/', views.emp_master, name='emp_master'),
]
