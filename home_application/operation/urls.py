# -*-coding:utf-8-*-
# _author_ = without
# _Date_ = 2019/4/15
# _Time_ = 15:35
# _IDE_ = PyCharm

from django.conf.urls import patterns


urlpatterns = patterns(
    'home_application.operation.views',
    (r'^business/$', 'business'),  # ��ȡҵ��ӿ�
    (r'^cluster/$', 'cluster'),  # ��ȡ��Ⱥ�Ľӿ�
    (r'^host/$', 'host'),  # ����ҵ���ȡ�����Ľӿ�
    (r'^run_script/$', 'run_script'),  # ִ�нű��ӿ�
)