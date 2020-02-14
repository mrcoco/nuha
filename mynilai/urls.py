"""mynilai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from frontend import views as FrontViews

admin.site.site_header = "SIAKAD NUHA Admin"
admin.site.site_title = "SIAKAD NUHA Admin Portal"
admin.site.index_title = "Sistem Informasi Akademik - SMK Ma'arif Nurul Haromain"

urlpatterns = [
    #path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    #path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('',FrontViews.index),
    path('login/', FrontViews.loginpage,name="user_login"),
    path('frontend/',include('frontend.urls')),
    path('raport/',include('raport.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

