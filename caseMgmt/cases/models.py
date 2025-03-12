from django.db import models
from users.models import User


def caseDocPath(instance, filename):
    return 'CaseDoc/case_{0}/{1}'.format(str(instance.case_belonged.id), filename)


def servDocPath(instance, filename):
    return 'CaseDoc/case_{0}/serv_{1}/{2}'.format(str(instance.serv_belonged.case_belonged.id),
                                                  str(instance.serv_belonged.id), filename)


class Case(models.Model):
    case_name = models.CharField('案件名', max_length=255)
    case_info = models.CharField('案件信息', max_length=512, blank=True, null=True)
    date_started = models.DateField('开始时间', auto_now_add=True)
    date_ended = models.DateField('结束时间', blank=True, null=True)
    state = models.BooleanField('完成状态', default=False)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='案件主管')


class Service(models.Model):
    service_name = models.CharField('服务名', max_length=255)
    service_info = models.CharField('服务信息', max_length=512, blank=True, null=True)
    date_started = models.DateField('开始日期', auto_now_add=True)
    date_ended = models.DateField('结束日期', blank=True, null=True)
    provider_name = models.CharField('供应商名', max_length=255)
    provider_contact_info = models.CharField('供应商联系方式', max_length=150, blank=True, null=True)
    state = models.BooleanField('完成状态', default=False)
    type = models.CharField('服务类型', default='11', max_length=20)
    case_belonged = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='所属案件')


class CaseDoc(models.Model):
    file = models.FileField(upload_to=caseDocPath)
    type = models.CharField('文档类型', default='1', max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    case_belonged = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='所属案件')


class ServDoc(models.Model):
    file = models.FileField(upload_to=servDocPath)
    type = models.CharField('文档类型', default='1', max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    serv_belonged = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='所属服务')
