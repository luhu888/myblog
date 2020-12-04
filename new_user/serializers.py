from rest_framework import serializers

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

