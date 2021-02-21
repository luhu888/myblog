import base64
from rest_framework import exceptions, viewsets, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from myAPI.models import APIActivityRelated, APIActivity
from myAPI.serializers import APIActivityRelatedSerializer, Register1Serializer, GetJoinListSerializer, \
    GetActivitySerializer, LoginSerializer, APISubstitutionSerializer
from new_user.models import BadmintonActivity, BadmintonActivityDetails, MyUser
import logging
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView, ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken
from datetime import datetime


logger = logging.getLogger('django')
week_change = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '日'}


class RegisterAPIView(generics.CreateAPIView):
    # 序列化类
    serializer_class = Register1Serializer
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
            user = MyUser.objects.create_user(username=username, password=password, weChat=weChat)
            user.save()
            # headers = self.get_success_headers(serializer.data)
            data = {'code': 200, 'msg': '注册成功', 'data': serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {'code': 400, 'msg': '注册失败', 'data': serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class JoinAPIViewSet(generics.CreateAPIView):
    """
    活动报名视图函数
    """
    # 序列化类
    serializer_class = APIActivityRelatedSerializer
    # 查询集和结果集
    queryset = BadmintonActivityDetails.objects.all()
    # 用户验证
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # serializer.data['is_substitution'] = True   # 报名替补
            self.create(serializer)
            count = APIActivityRelated.objects.filter(activity_number=serializer.data['activity_number']).count()
            limit = APIActivity.objects.get(activity_number=serializer.data['activity_number']).limit_count
            activity = APIActivity.objects.get(activity_number=serializer.data['activity_number'])
            if count >= limit:
                activity.is_full = True
            else:
                activity.is_full = False
            activity.save()
            logger.info(limit)
            headers = self.get_success_headers(serializer.data)
            data = {
                "msg": "success",
                "code": 200,
                "data": serializer.data

            }
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            logger.info(serializer.data)
            data = {
                "msg": "fail",
                "code": 400,
                "data": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class SubstitutionAPIViewSet(generics.CreateAPIView):
    """
    活动替补视图函数
    """
    # 序列化类
    serializer_class = APISubstitutionSerializer
    # 查询集和结果集
    queryset = BadmintonActivityDetails.objects.all()
    # 用户验证
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            logger.info(type(serializer.data))

            # serializer.data['is_substitution'] = True  # 报名替补
            logger.info(serializer.data)
            self.create(serializer)
            headers = self.get_success_headers(serializer.data)
            data = {
                "msg": "fail",
                "code": 400,
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            logger.info(serializer.data)
            try:
                data = {
                    "msg": "fail",
                    "code": 400,
                    "data": serializer.errors['non_field_errors']
                }
            except KeyError:
                data = {
                    "msg": "fail",
                    "code": 400,
                    "data": serializer.errors
                }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


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
    """
    登录报错处理
    :param serializer:
    :param request:
    :return:
    """
    return {
        "msg": "用户名或者密码错误",
        "code": 400,
        "errors": serializer.errors
    }


class MyJSONWebTokenAPIView(JSONWebTokenAPIView):
    """
    登录错误信息返回重写JSONWebTokenAPIView

    """
    serializer_class = LoginSerializer
    queryset = MyUser.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        """
        登录接口
        :param request:请求
        :param args:形参
        :param kwargs:关键字参数
        :return:登录成功就返回token，失败返回原因
        """
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
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


class MyObtainJSONWebToken(ObtainJSONWebToken, MyJSONWebTokenAPIView):
    pass


class MyRefreshJSONWebToken(RefreshJSONWebToken, MyJSONWebTokenAPIView):
    pass


class MyVerifyJSONWebToken(VerifyJSONWebToken, MyJSONWebTokenAPIView):
    pass


obtain_jwt_token = MyObtainJSONWebToken.as_view()
refresh_jwt_token = MyRefreshJSONWebToken.as_view()
verify_jwt_token = MyVerifyJSONWebToken.as_view()


class GetJoinList(generics.ListAPIView):

    # 序列化类
    serializer_class = GetJoinListSerializer

    # 查询集和结果集
    queryset = APIActivityRelated.objects.all()
    # 用户验证
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer = BadmintonActivityDetails.objects.get(activity_number=request.data['activity'])
            logger.info(serializer.data)
            data = {
                "msg": "success",
                "code": 200,
                "data": serializer.data

            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                "msg": "fail",
                "code": 400,
                "data": serializer.errors

            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

#
# class MyPagination(PageNumberPagination):
#     # 每页条数
#     page_size = 5
#     # 页数拼接参数名
#     page_query_param = 'page'
#     # page_size_query_param = 'size'
#     # max_page_size = 100


class GetJoinListView(generics.ListAPIView):
    """
    报名表维度的活动详情,目前没用
    """
    # 序列化类
    serializer_class = GetJoinListSerializer
    # 查询集和结果集

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = APIActivityRelated.objects.all()
        activity_number = self.request.query_params.get('activity_number', None)
        if activity_number is not None:
            queryset = queryset.filter(activity_number=activity_number)
        return queryset


class ActivityListView(generics.ListAPIView):
    """
    活动列表和详情视图,详情接口请在链接后加/?activity_name=name
    """
    serializer_class = GetActivitySerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = APIActivity.objects.all()
        activity_name = self.request.query_params.get('activity_name', None)
        if activity_name is not None:
            queryset = queryset.filter(activity_name=activity_name, is_alive=True)
        return queryset.filter(is_alive=True)

    def get(self, request, *args, **kwargs):
        ret = super().get(self,request,*args,**kwargs)
        if ret.data:
            data = {"msg": "success",
                    "code": 200,
                    "data": ret.data
                    }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"msg": "fail",
                    "code": 400,
                    "errors": '活动不存在'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
