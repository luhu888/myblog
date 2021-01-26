import logging

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from myAPI.models import APIActivity, APIActivityRelated
from new_user.models import MyUser
logger = logging.getLogger('django')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'username': {
                'help_text': '登录名'
            },
            'weChat': {
                'help_text': '微信昵称'

            },
            'password': {
                'help_text': '设置密码'
            },
        }
        model = MyUser
        # 要显示出来的字段
        fields = ('username', 'weChat', 'password')


class APIActivityRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'activity_number': {
                'help_text': '活动id'
            },
            'joiner': {
                'help_text': '报名人id'

            },
        }
        model = APIActivityRelated
        fields = ('activity_number', 'joiner')
        validators = [
            UniqueTogetherValidator(
                queryset=APIActivityRelated.objects.all(),
                fields=('activity_number', 'joiner'),
                message='该用户已报名，请勿重复报名',),

        ]


    def validate(self, data):
        is_operate = APIActivity.objects.get(activity_name=data['activity_number']).is_operate
        is_full = APIActivity.objects.get(activity_name=data['activity_number']).is_full
        is_cancel = APIActivity.objects.get(activity_name=data['activity_number']).is_cancel
        is_alive = APIActivity.objects.get(activity_name=data['activity_number']).is_alive
        if is_operate is False:
            raise serializers.ValidationError('活动报名已截止')
        elif is_full:
            raise serializers.ValidationError('该活动已订满，请报名替补')
        elif is_cancel:
            raise serializers.ValidationError("对不起，该活动已取消")
        elif is_alive:
            raise serializers.ValidationError("对不起该活动已结束")
        else:
            return data


