from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class MyUser(AbstractUser):
    weChat = models.CharField('微信账号', max_length=100, blank=True)

    def __str__(self):
        return self.username


class BadmintonActivity(models.Model):
    activity_name = models.CharField('活动名称', max_length=100)
    activity_start_time = models.DateTimeField('开始时间', default=timezone.now)
    activity_end_time = models.DateTimeField('结束时间', default=timezone.now)
    activity_number = models.IntegerField('活动编号', auto_created=True)
    is_alive = models.BooleanField('是否结束', default=False)

    class Meta:
        verbose_name = '活动列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.activity_name


class BadmintonActivityDetails(models.Model):
    activity_name = models.CharField('活动名称', max_length=100)
    join_weChat = models.IntegerField('报名人员', blank=True)
    is_alive = models.BooleanField('是否结束', default=False)

    class Meta:
        verbose_name = '活动详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.activity_name


