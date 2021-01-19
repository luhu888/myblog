from rest_framework import serializers
from blog.models import Category
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('name', 'index')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Category.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.index = validated_data.get('index', instance.index)
#         instance.save()
#         return instance


class CategorySerializer(serializers.ModelSerializer):
    """
    ModelSerializer类是创建序列化器类的快捷方式
    默认简单实现的create()和update()方法
    """
    class Meta:
        extra_kwargs = {
            'name': {
                'help_text': '这是名字，6～16位'

            },
            'index': {
                'help_text': '这是密码，6～16位'
            }
        }
        model = Category
        fields = ('name', 'index')


    # def to_representation(self, instance):    # 自定义返回每条数据的格式
    #     return {
    #         'code': 1, 'msg': '成功', 'errors': {}, 'data':
    #             { 'name': instance.name,
    #             'index': instance.index,
    #               }
        # }