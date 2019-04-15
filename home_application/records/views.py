# -*- coding: utf-8 -*-
# _author_ = without
# _Date_ = 2019/4/15
# _Time_ = 16:36
# _IDE_ = PyCharm
import datetime

from common.mymako import render_mako_context, render_json
from home_application import models


def shows(request):
    """
    历史记录的接口
    :param request:
    :return:
    """
    return render_mako_context(request, '/home_application/show_one.html')


def records(request):
    """
    记录展示的接口
    :param request:
    :return:
    """
    response = {}
    data_list = []
    # try:
    data = models.Records.objects.all()
    for i in data:
        dic = {'id': i.id, 'status': i.status, 'biz_name': i.biz_name, 'script_name': i.script_name,
               'start_time': i.start_time, 'ip': i.ip}
        data_list.append(dic)
    response["status"] = 0
    response["message"] = u'脚本执行成功'
    response["result"] = True
    response['data'] = data_list
    # except Exception as e:
    #     response["result"] = False
    #     response["status"] = 1
    #     response["message"] = u'脚本执行失败，失败原因：%s' % e
    #     response['data'] = []
    return render_json(response)


def search_records(request):
    """
    历史记录查询的接口
    :param request:
    :return:
    """
    response = {}
    bk_biz_name = request.GET.get('bk_biz_name')
    # bk_biz_name = '蓝鲸exam'
    time_1 = request.GET.get('time')
    # time_1 = '2019-04-08'
    obj = models.Records.objects.filter(biz_name=bk_biz_name,)
    data_list = []
    if obj:
        for i in obj:
            if time_1:
                if str(i.start_time[0:10]) == time_1:
                    dic = {'id': i.id, 'status': i.status, 'biz_name': i.biz_name, 'script_name': i.script_name,
                           'start_time': i.start_time, 'ip': i.ip}
                    data_list.append(dic)
            else:
                dic = {'id': i.id, 'status': i.status, 'biz_name': i.biz_name, 'script_name': i.script_name,
                       'start_time': i.start_time, 'ip': i.ip}
                data_list.append(dic)
    response['data'] = data_list
    return render_json(response)


def end(request):
    """
    关闭周期的接口
    :param request:
    :return:
    """
    response = {}
    records_id = request.GET.get('records_id')
    result = models.Records.objects.get(id=records_id)
    result.status = 0
    result.save()
    return render_json(response)


def start(request):
    """
    开启周期的接口
    :param request:
    :return:
    """
    response = {}
    records_id = request.GET.get('records_id')
    result = models.Records.objects.get(id=records_id)
    result.status = 1
    result.save()
    return render_json(response)


def details(request):
    """
    查看详情接口
    :param request:
    :return:
    """
    response = {}
    records_id = request.GET.get('records_id')
    # result = models.Records.objects.get(id=records_id)
    # data = result.log_content
    re = models.Host.objects.get(id=records_id)
    data = re.log_content
    response['data'] = data
    return render_json(response)

def dateRange(beginDate):
    """
    设计时间格式，也就是取出今天前七天的时间列表
    :param beginDate:
    :return:
    """
    yes_time = beginDate + datetime.timedelta(days=+1)
    aWeekDelta = datetime.timedelta(weeks=1)
    aWeekAgo = yes_time - aWeekDelta
    dates = []
    i = 0
    begin = aWeekAgo.strftime("%Y-%m-%d")
    dt = datetime.datetime.strptime(begin, "%Y-%m-%d")
    date = begin[:]
    while i < 7:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
        i += 1
    return dates


def num(request):
    """
    最近七天的执行次数
    :param request:
    :return:
    """
    response = {}
    num_list = [0 for x in range(0, 7)]
    dt_s = datetime.datetime.now()
    time_list = dateRange(dt_s)
    result = models.Records.objects.all()
    if result:
        for i in result:
            for j in time_list:
                if i.start_time:
                    if i.start_time[0:10] == j:
                        index = time_list.index(j)
                        num_list[index] += 1
    response['name'] = time_list
    response['value'] = num_list
    return render_json(response)


def num_htm(request):
    """
    返回图表的界面
    :param request:
    :return:
    """
    return render_mako_context(request, '/home_application/static_icon.html')


def dynamic(request):
    """
    动态展示数据的接口
    :param request:
    :return:
    """
    reaponse = {}
    host_id = request.GET.get('host_id')
    # host_id = 1
    Host_result = models.Host.objects.get(id=host_id)
    log_content = Host_result.log_content
    data_list = log_content.split('|')
    # memory = data_list[0]
    # disk = data_list[1]
    # cpu = data_list[2]
    reaponse['memory'] = data_list[0][0:-1]
    reaponse['disk'] = data_list[1][0:-1]
    reaponse['cpu'] = data_list[2][0:-2]
    return render_json(reaponse)


def dynamic_html(request):
    """
    展示动态展示页面
    :param request:
    :return:
    """
    host_id = request.GET.get('host_id')
    return render_mako_context(request, '/home_application/icon.html', {'host_id': host_id})


def de(request):
    """
    log的数据展示接口
    :param request:
    :return:
    """
    records_id = request.GET.get('re')
    # print records_id
    result = models.Host.objects.filter(task=records_id)
    data_list = []
    for i in result:
        dic = {'ip': i.ip, 'id': i.id, 'start_time': i.start_time, 'log_content': i.log_content}
        data_list.append(dic)
    return render_mako_context(request, '/home_application/show_two.html', {'data_list': data_list})