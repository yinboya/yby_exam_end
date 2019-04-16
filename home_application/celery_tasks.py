# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import base64
import datetime

from celery import task
from celery.task import periodic_task

from common.log import logger
from home_application import models
from home_application.utils import ESB

@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=1)
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    result = models.Records.objects.filter(status=1)
    if result.count() != 0:
        for i in result:
            ip_list = []
            # data = {}
            # data['bk_cloud_id'] = 0
            # data['ip'] = ip.encode('raw_unicode_escape')
            for j in i.ip.split(','):
                data = {}
                data['bk_cloud_id'] = 0
                data['ip'] = j
                ip_list.append(data)
            # script_param = base64.b64encode(i.set_name.encode('utf-8'))
            script_contents = models.Script.objects.get(name=i.script_name)
            script_data = base64.b64encode(script_contents.script_content.encode('utf-8'))
            records_id = i.id
            bk_biz_id = i.bk_biz_id
            async_run_script.delay(records_id=records_id, bk_biz_id=bk_biz_id, ip_list=ip_list,
                                   script_content=script_data, script_param=None)
    else:
        logger.info(u"暂无周期任务")
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))


@task
def async_run_script(records_id, bk_biz_id, script_content, ip_list, script_param):
    """
    快速执行脚本
    :param bk_biz_id:
    :param script_content:
    :param ip_list:
    :return:
    """
    records = models.Records.objects.filter(id=records_id)
    records = records[0]
    result = ESB.ESBComponentApi().fast_execute_script(bk_biz_id=bk_biz_id, script_content=script_content, ip_list=ip_list, script_type=1, script_param=script_param)
    if result["result"]:
        job_instance_id = result["data"]["job_instance_id"]
        get_script_log_data.apply_async(args=[records.id, bk_biz_id, job_instance_id], eta=datetime.datetime.now() + datetime.timedelta(seconds=5))

    return result


@task
def get_script_log_data(records_id, bk_biz_id, job_instance_id):
    try:
        records = models.Records.objects.filter(id=records_id)
        records = records[0]
        # task = models.Host.objects.filter(task=records_id)
        datas = ESB.ESBComponentApi().get_job_instance_log(bk_biz_id=bk_biz_id, job_instance_id=job_instance_id)
        if datas["data"][0]["status"] == 3:
            result = datas['data'][0]["step_results"]
            for i in result[0]['ip_logs']:
                ip = i["ip"]
                log_content = i["log_content"]
                start_time = i["start_time"]
                models.Host.objects.create(
                   task=records,
                   ip=ip,
                   log_content=log_content,
                   start_time=start_time
               )
            # records.log_content = log_content
            records.start_time = datas['data'][0]["step_results"][0]["ip_logs"][0]["start_time"][0:10]
            records.result = 3
            records.save()
        elif datas["data"][0]["status"] == 2:
            get_script_log_data.apply_async(args=[records.id, bk_biz_id, job_instance_id],
                                            eta=datetime.datetime.now() + datetime.timedelta(seconds=5))
        else:
            records.result = 1
            records.save()
    except Exception as e:
        logger.error(e)

