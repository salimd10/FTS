"""FTS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path, include
from FTS.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),

    #usr auth urls
    path('', home),
    path('add_staff/', add_staff),
    path('add_file/', add_file),
    path('add_staff_login/', add_staff_login),
    path('rmv_staff_login/', rmv_staff_login),
    re_path(r'^staff/(\d{1,4})/$', staff),
    re_path(r'^admin_staff/(\d{1,4})/$', admin_staff),
    re_path(r'^accept/(\d{1,4})', accept),
    re_path(r'^send/(\d{1,4})', send),
    re_path(r'^logout/$', logout),
    path('manage_logins/', manage_logins),
    path('search/', search),
    url(r'^select2/', include('django_select2.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
