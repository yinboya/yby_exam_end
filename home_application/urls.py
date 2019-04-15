# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^api/', include('home_application.utils.urls')),   # 测试接口
    (r'^operation/', include('home_application.operation.urls')),  # 执行操作的接口
    (r'^script/', include('home_application.script.urls')),  # 脚本管理的接口
    (r'^records/', include('home_application.records.urls')),  # 脚本管理的接口
)
