# -*-coding:utf-8-*-
# _author_ = without
# _Date_ = 2019/4/15
# _Time_ = 16:36
# _IDE_ = PyCharm
from django.conf.urls import patterns


urlpatterns = patterns(
    'home_application.records.views',
    (r'^shows/$', 'shows'),  # �ܼ�¼��ѯ����
    (r'^records/$', 'records'),  # ��¼չʾ�Ľӿ�
    (r'^search_records/$', 'search_records'),  # ��ѯ��¼�Ľӿ�
    (r'^dynamic/$', 'dynamic'),  # ��̬չʾ�ӿ�
    (r'^dynamic_html/$', 'dynamic_html'),  # ��̬չʾ�ӿ�
    (r'^num/$', 'num'),  # ��������ִ�д���
    (r'^num_htm/$', 'num_htm'),  # ͼ��չʾ
    (r'^start/$', 'start'),  # �������ڽӿ�
    (r'^end/$', 'end'),  # �ر����ڽӿ�
    (r'^details/$', 'details'),  # ��ȡִ������
    (r'^de/$', 'de'),  # ��������
    (r'^get_user/$', 'get_user'),  # ��������
)