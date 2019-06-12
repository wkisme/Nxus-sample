
#coding:utf-8
from django.conf.urls import url
 
from . import view
 
urlpatterns = [
    url(r'alldevice/$', view.alldevice),
    url(r'readcpu/$', view.readcpu)
]

