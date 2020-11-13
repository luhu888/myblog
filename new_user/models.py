from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# from django.contrib.auth.models import UserManager as _UserManager


class MyUser(AbstractUser):
    weChat = models.CharField('微信账号', max_length=100, blank=True, unique=True)
    # objects = UserManager()

    def __str__(self):
        return self.username


class BadmintonActivity(models.Model):
    activity_number = models.IntegerField('活动编号', auto_created=True)
    activity_name = models.CharField('活动名称', max_length=100)
    activity_start_time = models.DateTimeField('开始时间', default=timezone.now)
    activity_end_time = models.DateTimeField('结束时间', default=timezone.now)
    is_alive = models.BooleanField('是否结束', default=False)
    is_full = models.BooleanField('是否订满', default=False)
    limit_count = models.IntegerField('人数限制', default=100)

    class Meta:
        verbose_name = '活动列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.activity_name


class BadmintonActivityDetails(models.Model):
    activity_number = models.ForeignKey(BadmintonActivity, on_delete=models.CASCADE, verbose_name='活动编号', default=1)
    join_weChat = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='报名人员')
    is_substitution = models.BooleanField(verbose_name='是否替补', default=False)

    class Meta:
        unique_together = ('activity_number', 'join_weChat',)   # 多个字段联合唯一约束
        verbose_name = '活动详情'
        verbose_name_plural = verbose_name

    def __str__(self):   # 后台面包屑导航
        return ''


