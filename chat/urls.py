from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('home', views.home, name="home"),
    path('userReg', views.userReg, name="userReg"),
    path('userLogin', views.userLogin, name="userLogin"),
    path('logout', views.logout_view, name="logout"),
    path('idsent', views.idsent, name="idsent"),
    path('idset/<identity>', views.idset, name="idset"),
    path('msg', views.msg, name="msg"),
    path('msgSent', views.msgSent, name="msgSent"),
]