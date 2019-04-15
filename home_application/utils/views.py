# -*-coding:utf-8-*-
# _author_ = without
# _Date_ = 2019/4/9
# _Time_ = 15:56
# _IDE_ = PyCharm
from common.mymako import render_json


def test(request):
    response = {}
    response['name'] = 'test'
    response['user_name'] = 'yin'
    response['status'] = 1
    return render_json(response)
