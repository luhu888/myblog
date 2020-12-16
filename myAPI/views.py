import base64
import logging

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from myAPI.models import APIActivityRelated
from myAPI.serializers import RegisterSerializer, APIActivityRelatedSerializer
from new_user.models import MyUser


logger = logging.getLogger('django')


class RegisterAPIView(generics.CreateAPIView):
    # 序列化类
    serializer_class = RegisterSerializer
    # 查询集和结果集
    queryset = MyUser.objects.all()
    # 用户验证
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data['password']
        username = serializer.data['username']
        weChat1 = serializer.data['weChat']
        weChat2 = base64.b64encode(weChat1.encode('utf8'))
        weChat = str(weChat2, 'utf-8')
        user = MyUser.objects.create_user(username=username, password=password, weChat=weChat)
        user.save()
        # headers = self.get_success_headers(serializer.data)
        data = {'code': 200, 'msg': '注册成功', 'data': serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)


class JoinAPIViewSet(generics.CreateAPIView):
    # 序列化类
    serializer_class = APIActivityRelatedSerializer
    # 用户验证
    queryset = APIActivityRelated.objects.all()

    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # activity_number = serializer.data['activity_number']

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
