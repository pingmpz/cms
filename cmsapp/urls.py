from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login_action/', views.login_action, name='login_action'),
    path('logout_action/', views.logout_action, name='logout_action'),
    path('index/', views.index, name='index'),
    path('new_request/', views.new_request, name='new_request'),
]
