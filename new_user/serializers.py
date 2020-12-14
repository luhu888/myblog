from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from new_user.models import MyUser, BadmintonActivityDetails


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


class JoinSerializer(serializers.ModelSerializer):
    """SlugRelatedField 可以使用目标上的字段来表示关系的目标"""

    tracks = serializers.SlugRelatedField(many=True, read_only=True, slug_field='is_full')

    class Meta:
        extra_kwargs = {
            'activity_number': {
                'help_text': '活动编号'
            },
            'join_weChat': {
                'help_text': '微信号'

            },

        }
        model = BadmintonActivityDetails
        # 要显示出来的字段
        fields = ['activity_number', 'join_weChat', 'tracks']

        validators = [
            UniqueTogetherValidator(
                queryset=BadmintonActivityDetails.objects.all(),
                fields=['activity_number', 'join_weChat'],
                message='该用户已报名，请勿重复报名',
            ),

        ]

