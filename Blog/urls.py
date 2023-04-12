"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from BlogPost import urls as BlogPostUrls
from django.shortcuts import render,redirect
from authHandler.views import LoginView,LogoutView,UserCreationView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__',include('debug_toolbar.urls')), # adding some special path to urlpatterns
    path('api/',include(BlogPostUrls)),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('user/',UserCreationView.as_view(),name="createUser"),
    path('',lambda request:render(request=request,template_name='index.html'))
]

# adding some special path to urlpatterns
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)