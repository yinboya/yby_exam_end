# -*-coding:utf-8-*-
# _author_ = without
# _Date_ = 2019/4/15
# _Time_ = 15:35
# _IDE_ = PyCharm

from django.conf.urls import patterns


urlpatterns = patterns(
    'home_application.operation.views',
    (r'^business/$', 'business'),  # 获取业务接口
    (r'^cluster/$', 'cluster'),  # 获取集群的接口
    (r'^host/$', 'host'),  # 根据业务获取主机的接口
    (r'^run_script/$', 'run_script'),  # 执行脚本接口
)