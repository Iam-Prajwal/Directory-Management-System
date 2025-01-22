"""
URL configuration for directorymgmt project.

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
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('Dashboard', views.DASHBOARD, name='dashboard'),
    path('Login', views.LOGIN, name='login'),
    path('', views.Index, name='index'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),
    path('AdminProfile', views.ADMIN_PROFILE, name='admin_profile'),
    path('AdminProfile/update', views.ADMIN_PROFILE_UPDATE, name='admin_profile_update'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),
    path('AddData', views.ADD_DATA, name='add_data'),
    path('ManageData', views.MANAGE_DATA, name='manage_data'),
   
    path('DeleteData/<str:id>', views.DELETE_DATA, name='delete_data'),
    path('ViewData/<str:id>', views.VIEW_DATA, name='view_data'),
    path('EditData', views.EDIT_DATA, name='edit_data'),
    path('AllRecords', views.ALL_RECORDS, name='all_records'),
    path('PublicAllRecords', views.PUBLIC_RECORDS, name='public_records'),
    path('PrivateAllRecords', views.PRIVATE_RECORDS, name='private_records'),
    path('SearchRecords', views.SEARCH_RECORDS, name='search_records'),
    path('ReportRecords', views.RECORDS_REPORTS, name='records_reports'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
