# -*- coding: utf-8 -*-
# _author_ = without
# _Date_ = 2019/4/15
# _Time_ = 16:30
# _IDE_ = PyCharm
from home_application import models
from common.mymako import render_json, render_mako_context
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def select_script(request):
    """
    选择脚本的接口
    :param request:
    :return:
    """
    response = {}
    l_s = []
    try:
        data = models.Script.objects.all()
        if data:
            for i in data:
                dic = {'id': i.id, 'name': i.name}
                l_s.append(dic)
            response['code'] = 0
            response['message'] = 'success'
            response['data'] = l_s
        else:
            response['code'] = 0
            response['message'] = u'没有脚本'
            response['data'] = []
    except Exception, e:
        response['code'] = 1
        response['message'] = '%s' % e
        response['data'] = []
    return render_json(response)


def script_management(request):
    """
    脚本展示的接口
    :param request:
    :return:
    """
    all_script_data = models.Script.objects.all()
    return render_mako_context(request, '/home_application/script.html', {'all_script_data': all_script_data})


def add_script(request):
    """
    添加脚本的接口
    :param request:
    :return:
    """
    name = request.GET.get('script_name')
    content = request.GET.get('script_content')
    models.Script.objects.create(
        name=name,
        script_content=content
    )
    return redirect(reverse(script_management))


def delete_script(request, script_id):
    """
    删除脚本的接口
    :param request:
    :return:
    """
    # todo  不用进行get操作
    script_data = models.Script.objects.get(id=script_id)
    script_data.delete()
    # todo 调研一下
    return redirect(reverse(script_management))
