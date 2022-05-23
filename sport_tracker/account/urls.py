from django.urls import include, re_path
from account import views

urlpatterns = [
    re_path(r'^register/$', views.UserRegisterView.as_view(), name='register'),

]
