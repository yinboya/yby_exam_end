# _*_ coding:utf-8 _*_
from django.db import models


class Script(models.Model):
    name = models.CharField(verbose_name=u'脚本名称', max_length=100)
    script_content = models.TextField(verbose_name=u'脚本内容', null=True)

    class Meta:
        verbose_name = u'脚本表'
        verbose_name_plural = u'脚本表'
        db_table = 'script'


class Records(models.Model):
    bk_biz_id = models.IntegerField(verbose_name=u'业务ID', null=True)
    biz_name = models.CharField(verbose_name=u'业务名称', max_length=200, null=True)
    set_id = models.IntegerField(verbose_name=u'集群id', null=True)
    set_name = models.CharField(verbose_name=u'集群名称', max_length=200, null=True)
    ip = models.CharField(verbose_name=u'主机的ip地址', max_length=500, null=True)
    start_time = models.CharField(max_length=200, verbose_name=u'脚本执行开始时间', null=True)
    # log_content = models.TextField(verbose_name=u'脚本执行日志', null=True)
    result = models.IntegerField(verbose_name=u'脚本执行结果', null=True)
    # 成功为3， 失败为1
    status = models.IntegerField(verbose_name=u'是否开启周期', null=True)
    # 默认为0 不开启   1 为开启
    script_name = models.CharField(verbose_name=u'脚本ID', max_length=200, null=True)
    user = models.CharField(verbose_name=u'操作人', max_length=200)

    class Meta:
        verbose_name = u'脚本记录表'
        verbose_name_plural = u'脚本记录表'
        db_table = 'records'


class Host(models.Model):
    task = models.ForeignKey(Records, verbose_name=u'执行的记录')
    ip = models.CharField(verbose_name=u'对应的ip', max_length=200)
    start_time = models.CharField(verbose_name=u'开始时间', max_length=200)
    log_content = models.CharField(verbose_name=u'执行日志', max_length=500)

    class Meta:
        verbose_name = u"获取脚本执行记录"
        db_table = 'host'
