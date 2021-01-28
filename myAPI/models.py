from django.db import models
from django.utils import timezone
from new_user.models import MyUser


class APIActivity(models.Model):
    activity_number = models.IntegerField('活动编号', auto_created=True)
    activity_name = models.CharField('活动名称', max_length=100)
    activity_start_time = models.DateTimeField('开始时间', default=timezone.now)
    activity_end_time = models.DateTimeField('结束时间', default=timezone.now)
    is_alive = models.BooleanField('是否结束', default=False)
    is_full = models.BooleanField('是否订满', default=False)
    limit_count = models.IntegerField('人数限制', default=100)
    activity_place = models.CharField('活动地点', max_length=100, default='')
    is_cancel = models.BooleanField('活动取消', default=False)
    is_operate = models.BooleanField('可取消报名', default=True)
    place_number = models.CharField('场地号', max_length=100, default='')

    class Meta:
        verbose_name = '活动列表'
        verbose_name_plural = verbose_name   # 不加会在后台显示文案加s

    def __str__(self):
        return self.activity_name


class APIActivityRelated(models.Model):
    joiner = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='报名人员',
                               related_name='joiners')  # on_delete级联删除
    is_substitution = models.BooleanField(verbose_name='是否替补', default=False)
    activity_number = models.ForeignKey(APIActivity, on_delete=models.CASCADE, verbose_name='活动编号', default=1,
                                        related_name='activities')
    operate_time = models.DateTimeField(verbose_name='操作时间', default=timezone.now)

    class Meta:
        unique_together = ('activity_number', 'joiner', 'is_substitution')   # 多个字段联合唯一约束
        verbose_name = '活动详情'
        verbose_name_plural = verbose_name

    def __str__(self):   # 后台面包屑导航
        return ''
