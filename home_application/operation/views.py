# -*-coding:utf-8-*-
# _author_ = without
# _Date_ = 2019/4/15
# _Time_ = 15:36
# _IDE_ = PyCharm
import base64
from common.mymako import render_json
from home_application.utils import ESB
from home_application import models
from home_application.celery_tasks import async_run_script

def business(request):
    """
    获取业务的接口
    :param request:
    :return:
    """
    response = {}
    data_list = []
    try:
        result = ESB.ESBApi(request).search_business()
        if result['result']:
            response['result'] = True
            response['code'] = 0
            response['message'] = 'success'
            response['data'] = {}
            if len(result['data']['info']) > 0:
                for item in result['data']['info']:
                    dic = {'id': item['bk_biz_id'], 'name': item['bk_biz_name']}
                    data_list.append(dic)
                    response['data'] = data_list
        else:
            response['result'] = True
            response['code'] = 0
            response['message'] = u'该用户下没有业务'
            response['data'] = {}
    except Exception, e:
        response['result'] = False
        response['code'] = 1
        response['message'] = u'获取业务列表失败：%s'  %e
        response['data'] = {}
    return render_json(response)


def cluster(request):
    """
    根据业务获取集群的接口
    :param request:
    :return:
    """
    response = {}

    try:
        # biz_id = request.GET.get("bk_biz_id")
        biz_id = 7
        result = ESB.ESBApi(request).search_set(bk_biz_id=int(biz_id))
        if result['result']:
            response['result'] = True
            response['code'] = 0
            response['message'] = 'success'
            response['data'] = {}
            list = []
            if len(result['data']['info']) > 0:
                for item in result['data']['info']:
                    listDic = {}
                    listDic['set_id'] = item['bk_set_id']
                    listDic['set_name'] = item['bk_set_name']

                    list.append(listDic)

                response['data']['list'] = list
            else:
                response['result'] = True
                response['code'] = 0
                response['message'] = u'该用户下无业务'
                response['data'] = {}
        else:
            response = result

    except Exception, e:
        response['result'] = False
        response['code'] = 1
        response['message'] = u'获取业务列表失败：%s' % e
        response['data'] = {}

    return render_json(response)


def host(request):
    """
    根据业务获取主机的接口
    :param request:
    :param bk_biz_id:
    :return:
    """
    bk_biz_id = request.GET.get('bk_biz_id')
    # set_id = request.GET.get('set_id')
    response = {}
    try:
        result = ESB.ESBApi(request).search_host(biz_id=bk_biz_id)
        list = []
        if result:
            response['result'] = True
            response['code'] = 0
            response['message'] = 'success'
            response['data'] = []
            if result['data']['count'] > 0:
                for i in result['data']['info']:
                    # for j in i['set']:
                    #     if int(j['bk_set_id']) == int(set_id):
                    dic = {'hostname': i['host']['bk_host_name'], 'ip': i['host']['bk_host_innerip'],
                           'os_type': i['host']['bk_os_type'], 'os_name': i['host']['bk_os_name']}
                    bk_cloud = i['host']['bk_cloud_id']
                    dic['area'] = bk_cloud[0]['bk_inst_name']
                    dic['area_id'] = bk_cloud[0]['bk_inst_id']
                    list.append(dic)
                response['result'] = True
                response['code'] = 0
                response['message'] = 'success'
                response['data'] = list
            else:
                response['result'] = True
                response['code'] = 0
                response['message'] = u'没有主机'
                response['data'] = []
    except Exception, e:
        response['result'] = False
        response['code'] = 1
        response['message'] = '%s' % e
        response['data'] = []
    return render_json(response)


def run_script(request):
    """
    执行导出脚本的接口
    """
    response = {}
    try:
        bk_biz_id = request.GET.get('bk_biz_id')
        # set_id = request.GET.get('set_id')
        ip = request.GET.get('ip_list')
        script_id = request.GET.get('script_id')
        biz_name = request.GET.get('biz_name')
        # set_name = request.GET.get('set_name')
        # input_url = request.GET.get('input_url')
        script_contents = models.Script.objects.get(id=script_id)
        script_data = base64.b64encode(script_contents.script_content.encode('utf-8'))
        ip_list = []
        # script_param = base64.b64encode(input_url.encode('utf-8'))
        # todo: 获取前段的数组
        if len(ip) > 14:
            ips = ip.split(",")
            for i in ips:
                data = {}
                # TODO 不能确定为0
                data['bk_cloud_id'] = 0
                data['ip'] = i.encode('raw_unicode_escape')
                ip_list.append(data)
        else:
            data = {}
            data['bk_cloud_id'] = 0
            # todo   .encode是否需要
            data['ip'] = ip.encode('raw_unicode_escape')
            ip_list.append(data)
        #todo 加一个事务
        records = models.Records.objects.create(
            bk_biz_id=bk_biz_id,
            # set_id=set_id,
            ip=ip,
            # set_name=set_name,
            # set_name=input_url,
            biz_name=biz_name,
            status=0,
            script_name=script_contents.name,
        )
        async_run_script.delay(records_id=records.id, bk_biz_id=bk_biz_id, ip_list=ip_list, script_content=script_data, script_param=None)
        response["status"] = 0
        response["message"] = u'脚本执行成功'
        response["result"] = True
    except Exception as e:
        response["result"] = False
        response["status"] = 1
        response["message"] = u'脚本执行失败，失败原因：%s' % e
    return render_json(response)