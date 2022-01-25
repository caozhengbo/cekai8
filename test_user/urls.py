from django.urls import path,re_path
from test_user import views

urlpatterns = [
    re_path(r'login/', views.login),
    re_path(r'register/',views.register)
]