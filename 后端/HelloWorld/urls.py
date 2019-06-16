# -*- coding: UTF-8 -*-

from django.conf.urls import url
 
from . import view
 
urlpatterns = [
    url(r'alldevice/$', view.alldevice),
    url(r'readcpu/$', view.readcpu),
    url(r'readflow/$', view.readflow),
    url(r'setconfig/$', view.setconfig),
    url(r'getconfig/$', view.getconfig),
    url(r'deleteconfig/$', view.deleteconfig),
    url(r'getproc/$', view.getproc)
]

