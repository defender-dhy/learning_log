'''为应用程序users定义url模式'''

from django.conf.urls import url
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    # 登录页面 LoginView.as_view后面要加上()
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'),name='login'), 

    # 注销
    url(r'^logout/$', views.logout_view, name='logout'),

    # 注册页面
    url(r'^register/$', views.register, name='register'),
]