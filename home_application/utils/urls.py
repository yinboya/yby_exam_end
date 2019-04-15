# -*-coding:utf-8-*-
# _author_ = without
# _Date_ = 2019/4/9
# _Time_ = 15:56
# _IDE_ = PyCharm

from django.conf.urls import patterns


urlpatterns = patterns(
    'home_application.utils.views',
    (r'^test/$', 'test'),  # 获取业务接口
)
