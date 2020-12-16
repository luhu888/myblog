from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from myAPI.models import APIActivity, APIActivityRelated
from new_user.models import MyUser


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
        model = APIActivityRelated
        fields = ['activity_number', 'joiner']
        validators = [
            UniqueTogetherValidator(
                queryset=APIActivityRelated.objects.all(),
                fields=['activity_number', 'joiner'],
                message='该用户已报名，请勿重复报名',),

        ]

    def validate(self, data):
        is_exist = APIActivity.objects.filter(activity_name=data['activity_number'], is_operate=False)
        if is_exist:
            raise serializers.ValidationError('活动截止')
        else:
            return data
