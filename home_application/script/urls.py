# -*-coding:utf-8-*-
# _author_ = without
# _Date_ = 2019/4/15
# _Time_ = 16:30
# _IDE_ = PyCharm

from django.conf.urls import patterns


urlpatterns = patterns(
    'home_application.script.views',
    (r'^select_script/$', 'select_script'),  # ѡ��ű��Ľӿ�
    (r'^script_management/$', 'script_management'),  # �ű��б�Ľӿ�
    (r'^add_script/$', 'add_script'),  # ��ӽű��Ľӿ�
    (r'^delete_script/(\d+)$', 'delete_script'),  # ɾ���ű��Ľӿ�
)