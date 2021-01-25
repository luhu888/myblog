import base64

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import exceptions, viewsets, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from new_user.models import BadmintonActivity, BadmintonActivityDetails, MyUser
from django.contrib.auth import login, logout, authenticate
import logging
from django.views.decorators.csrf import csrf_exempt
from new_user.serializers import RegisterSerializer, JoinSerializer
import re
from django.contrib.auth.backends import ModelBackend
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView, ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('django')
week_change = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '日'}


class RegisterAPIView(generics.CreateAPIView):
    # 序列化类
    serializer_class = RegisterSerializer
    # 查询集和结果集
    queryset = MyUser.objects.all()
    # 用户验证
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = serializer.data['password']
            username = serializer.data['username']
            weChat1 = serializer.data['weChat']
            weChat2 = base64.b64encode(weChat1.encode('utf8'))
            weChat = str(weChat2, 'utf-8')
            user = User.objects.create_user(username=username, password=password, weChat=weChat)
            user.save()
            # headers = self.get_success_headers(serializer.data)
            data = {'code': 200, 'msg': '注册成功', 'data': serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {'code': 400, 'msg': '注册失败', 'data': serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class JoinAPIViewSet(generics.CreateAPIView):
    # 序列化类
    serializer_class = JoinSerializer
    # 查询集和结果集
    queryset = BadmintonActivityDetails.objects.all()
    # 用户验证
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def jwt_response_payload_handler(token, user=None, request=None):
    """为返回的结果添加用户相关信息"""
    return {
        "msg": "success",
        "code": 200,
        "data": {
            "token": token,
            "user_id": user.id,
            "username": user.username
        }
    }


def jwt_response_payload_error_handler(serializer, request=None):
    return {
        "msg": "用户名或者密码错误",
        "code": 400,
        "errors": serializer.errors
    }


class MyJSONWebTokenAPIView(JSONWebTokenAPIView):
    """
    登录错误信息返回重写JSONWebTokenAPIView
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            logger.info(serializer.object.get('user'))
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response
        error_data = jwt_response_payload_error_handler(serializer, request)
        return Response(error_data, status=status.HTTP_200_OK)


class MyObtainJSONWebToken(ObtainJSONWebToken, MyJSONWebTokenAPIView):
    pass


class MyRefreshJSONWebToken(RefreshJSONWebToken, MyJSONWebTokenAPIView):
    pass


class MyVerifyJSONWebToken(VerifyJSONWebToken, MyJSONWebTokenAPIView):
    pass


obtain_jwt_token = MyObtainJSONWebToken.as_view()
refresh_jwt_token = MyRefreshJSONWebToken.as_view()
verify_jwt_token = MyVerifyJSONWebToken.as_view()
