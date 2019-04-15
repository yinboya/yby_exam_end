# -*-coding:utf-8-*-
# _author_ = without
# _Date_ = 2019/4/15
# _Time_ = 16:30
# _IDE_ = PyCharm

from django.conf.urls import patterns


urlpatterns = patterns(
    'home_application.script.views',
    (r'^select_script/$', 'select_script'),  # 选择脚本的接口
    (r'^script_management/$', 'script_management'),  # 脚本列表的接口
    (r'^add_script/$', 'add_script'),  # 添加脚本的接口
    (r'^delete_script/(\d+)$', 'delete_script'),  # 删除脚本的接口
)