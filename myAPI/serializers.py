import base64
import logging
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from myAPI.models import APIActivity, APIActivityRelated
from new_user.models import MyUser

logger = logging.getLogger('django')

class Register1Serializer(serializers.ModelSerializer):
    """
    注册序列化
    """
    class Meta:
        model = MyUser
        # 要显示出来的字段
        fields = ('username', 'weChat', 'password')
        extra_kwargs = {
            'username': {
                'help_text': '登录名',
                'required': True
            },
            'weChat': {

                'help_text': '微信昵称',
                'required': True
            },
            'password': {
                'help_text': '设置密码',
                'required': True
            },
        }


class APIActivityRelatedSerializer(serializers.ModelSerializer):
    """
    活动报名序列化
    """
    class Meta:
        extra_kwargs = {
            'activity_number': {
                'help_text': '活动id',
                'required': True
            },
            'joiner': {
                'help_text': '报名人id',
                'required': True

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
        is_exist = APIActivity.objects.get(activity_name=data['activity_number'])

        if is_exist:
            if is_operate is False:
                raise serializers.ValidationError('活动报名已截止')
            elif is_full:
                raise serializers.ValidationError('该活动已订满，请报名替补')
            elif is_cancel:
                raise serializers.ValidationError("对不起，该活动已取消")
            elif is_alive is False:
                raise serializers.ValidationError("对不起该活动已结束")
            else:
                return data
        else:
            raise serializers.ValidationError("对不起,您报名的活动不存在")


class APIActivitySerializer(serializers.ModelSerializer):
    """
    支持活动列表及详情序列化的序列化
    """
    class Meta:
        model = APIActivity
        fields = ('activity_number', 'is_alive', 'activity_place','activity_name')


class GetJoinListSerializer(APIActivitySerializer):
    """
    报名表维度活动详情序列化
    """
    join_name = serializers.CharField(source='joiner.weChat')
    activities = APIActivitySerializer(source='activity_number')  # source为外键对应的字段名

    class Meta:
        extra_kwargs = {
            'activity_number': {
                'help_text': '活动id',
                'required': True
            },
            'joiner': {
                'help_text': '报名人id',
                'required': True
            },
        }

        model = APIActivityRelated
        fields = ('join_name', 'activities')


    def to_representation(self, instance):
        """
        对返回的微信昵称解码处理后返回
        :param instance:
        :return:
        """
        data = super().to_representation(instance)
        data['join_name'] = base64.b64decode(data['join_name']).decode('utf8')
        return data

    def validate(self, data):
        logger.info(data)
        is_exist = APIActivity.objects.get(activity_name=data['activity_number'])
        if is_exist:
            return data
        else:
            raise serializers.ValidationError("对不起,您查询的活动不存在")


class GetActivitySerializer(serializers.ModelSerializer):
    """
    活动列表及详情序列化
    """
    activities = APIActivityRelatedSerializer(many=True)
    class Meta:
        model = APIActivity
        fields = ('activity_name', 'is_alive', 'activity_place', 'place_number',
                  'is_full', 'is_operate', 'limit_count','activity_start_time', 'activity_end_time', 'activities')

    def to_representation(self, instance):
        """
        将用户id转换成用户昵称
        :param instance:
        :return:
        """
        data = super().to_representation(instance)
        for joiner in data['activities']:
            logger.info(MyUser.objects.get(id=joiner['joiner']))
            weChat = str(MyUser.objects.get(id=joiner['joiner']).weChat)
            joiner['joiner'] = base64.b64decode(weChat).decode('utf8')
        return data







