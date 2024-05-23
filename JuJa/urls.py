"""
URL configuration for DjangoWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'JuJa'

urlpatterns = [
    path('', views.index, name='index'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register_user/', views.register_user, name='register_user'),
    path('make_invoice/', views.make_invoice, name='make_invoice'),
    path('view_invoices/', views.view_invoices, name='view_invoices'),
    path('view_invoice/<int:invoice_id>/', views.view_invoice, name='view_invoice'),
    path('edit_invoice/<int:invoice_id>/', views.edit_invoice, name='edit_invoice'),
    path('delete_invoice/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('enter_information/', views.enter_information, name='enter_information'),
    path('delete_invoices/', views.delete_invoices, name='delete_invoices'),
    path('make_write_off/', views.make_write_off, name='make_write_off'),
    path('view_write_offs/', views.view_write_offs, name='view_write_off'),
    path('view_write_off/<int:write_off_id>/', views.view_write_off, name='view_write_off'),
]
