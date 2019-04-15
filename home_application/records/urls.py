# -*-coding:utf-8-*-
# _author_ = without
# _Date_ = 2019/4/15
# _Time_ = 16:36
# _IDE_ = PyCharm
from django.conf.urls import patterns


urlpatterns = patterns(
    'home_application.records.views',
    (r'^shows/$', 'shows'),  # 总记录查询界面
    (r'^records/$', 'records'),  # 记录展示的接口
    (r'^search_records/$', 'search_records'),  # 查询记录的接口
    (r'^dynamic/$', 'dynamic'),  # 动态展示接口
    (r'^dynamic_html/$', 'dynamic_html'),  # 动态展示接口
    (r'^num/$', 'num'),  # 最近七天的执行次数
    (r'^num_htm/$', 'num_htm'),  # 图标展示
    (r'^start/$', 'start'),  # 开启周期接口
    (r'^end/$', 'end'),  # 关闭周期接口
    (r'^details/$', 'details'),  # 获取执行详情
    (r'^de/$', 'de'),  # 主机详情
)