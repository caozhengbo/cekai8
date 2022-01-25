"""cekai8 URL Configuration

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
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include("test_user.urls")),
    path('api/testrunner/', include("test_runner.urls")),

    # 需要在vue进行页面切换的路由
    # TemplateVive
    # path('testrunner/login', TemplateView.as_view(template_name='index.html')),
    # path('testrunner/register', TemplateView.as_view(template_name='index.html')),
    # path("testrunner/", TemplateView.as_view(template_name='index.html')),

    # 解决刷新页面丢失问题
    re_path(r'^testrunner/', TemplateView.as_view(template_name="index.html")),

]

a = False
