import base64

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import exceptions, viewsets, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from new_user.models import MyUser as User  # 扩展user后使用新的MyUser
from new_user.models import BadmintonActivity, BadmintonActivityDetails, MyUser
from django.contrib.auth import login, logout, authenticate
import logging
from django.views.decorators.csrf import csrf_exempt
from new_user.serializers import RegisterSerializer, JoinSerializer
import re
from new_user import models
from django.contrib.auth.backends import ModelBackend
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView, ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('django')
week_change = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '日'}


# 用户登录
def loginView(request):    # 设置标题和另外两个URL链接
    title = '登录'
    unit_2 = '/new_user/register.html'
    unit_2_name = '立即注册'
    unit_1 = '/new_user/setpassword.html'
    unit_1_name = '修改密码'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    logger.info('账号是有效的')
                    logger.info(user)
                    login(request, user)
                    return redirect('/')
            else:
                logger.info('账号密码错误，请重新输入')
                tips = '账号密码错误，请重新输入'
        else:
            logger.info('用户不存在')
            tips = '用户不存在，请注册'
    return render(request, 'user.html', locals())


def registerView(request):
    # 设置标题和另外两个URL链接
    title = '注册'
    unit_2 = '/new_user/login.html'
    unit_2_name = '立即登录'
    unit_1 = '/new_user/setpassword.html'
    unit_1_name = '修改密码'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        weChat1 = request.POST.get('weChat', '')
        weChat2 = base64.b64encode(weChat1.encode('utf8'))
        weChat = str(weChat2, 'utf-8')
        username_check = User.objects.filter(username=username)
        weChat_check = User.objects.filter(weChat=weChat)
        password = request.POST.get('password', '')
        if username_check or weChat_check:
            tips = '用户已存在'
        elif username == '' or weChat1 == '' or password == '':
            tips = '请将注册信息填写完整'
        else:
            user = User.objects.create_user(username=username, password=password, weChat=weChat)
            user.save()
            tips = '注册成功，请登录'
        del weChat_check
        del username_check
    return render(request, 'user.html', locals())


def setpasswordView(request):
    new_password = True
    title = '修改密码'
    unit_2 = '/new_user/login.html'
    unit_2_name = '立即登录'
    unit_1 = '/new_user/register.html'
    unit_1_name = '立即注册'

    if request.method == 'POST':
        username = request.POST.get('username', '')
        old_password = request.POST.get('password', '')
        new_password = request.POST.get('new_password', '')
        # 判断用户是否存在
        user = User.objects.filter(username=username)
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=old_password)
        # 判断用户的账号密码是否正确
        if user:
            # 密码加密处理并保存到数据库
            dj_ps = make_password(new_password, None, 'pbkdf2_sha256')
            user.password = dj_ps
            user.save()
        else:
            print('原始密码不正确')
    return render(request, 'user.html', locals())


def logoutView(request):
    logout(request)
    return redirect('/')


def check_login(func):  # 自定义登录验证装饰器
    def warpper(request, *args, **kwargs):
        is_login = request.session.get('is_login', False)
        if is_login:
            func(request, *args, **kwargs)
        else:
            return redirect("/")
    return warpper

@login_required
def activityView(request, number):
    activity_id = BadmintonActivity.objects.get(activity_number=number).id
    logger.info(activity_id)
    username = request.user.username
    activityDetails = BadmintonActivityDetails.objects.filter(activity_number_id=int(activity_id))
    join_dic = {}
    new_join_dic = []
    is_join = BadmintonActivityDetails.objects.filter(activity_number_id=int(activity_id), join_weChat_id=request.user.id, is_substitution=False)
    is_substitution = BadmintonActivityDetails.objects.filter(activity_number_id=int(activity_id), join_weChat_id=request.user.id, is_substitution=True)
    is_full = BadmintonActivity.objects.filter(activity_number=int(number)).values_list('is_full')[0][0]
    action = request.POST.get("action", '')
    join_dic = dict(BadmintonActivityDetails.objects.filter(activity_number_id=int(activity_id)).values_list('join_weChat', 'is_substitution').order_by('is_substitution'))
    logger.info(join_dic)
    activity_end_time = BadmintonActivity.objects.get(activity_number=int(number)).activity_end_time.strftime('%H:%M')
    activity_start_time = BadmintonActivity.objects.get(activity_number=int(number)).activity_start_time.strftime("%Y-%m-%d %H:%M")
    activity_week = BadmintonActivity.objects.get(activity_number=int(number)).activity_start_time.isoweekday()
    activity_time = str(activity_start_time) + '-' + str(activity_end_time) + ' 周' + week_change[str(activity_week)]
    activity_place = str(BadmintonActivity.objects.get(activity_number=int(number)).activity_place)
    limit_count = BadmintonActivity.objects.get(activity_number=int(number)).limit_count
    join_count = BadmintonActivityDetails.objects.filter(activity_number_id=int(activity_id)).count()  # is_substitution=0
    is_operate = BadmintonActivity.objects.get(activity_number=int(number)).is_operate
    surplus = limit_count - join_count
    if surplus <= 0:
        surplus = '0'
    else:
        surplus=str(surplus)
    logger.info(activity_place)
    # for i in activityDetails:
    for j in join_dic.keys():
        new_join_dic.append([base64.b64decode(MyUser.objects.get(id=j).weChat).decode('utf8'), join_dic[j]])
    if request.method == 'POST':
        if bool(is_join) and action == 'join':
            tips = '您已成功报名，请勿重复报名'
            logger.info(tips)
        elif action == 'join':
            if is_full:
                tips = '该活动已订满'
            else:
                tips = '报名成功'
                join_person = BadmintonActivityDetails(join_weChat_id=request.user.id, activity_number_id=int(activity_id))
                join_person.save()
        elif action == 'cancel':
            if is_operate:
                tips = '取消报名成功！'
                cancel_activity = BadmintonActivityDetails.objects.filter(activity_number_id=int(activity_id), join_weChat_id=request.user.id).delete()
                # logger.info(txt1)
            else:
                tips = '活动开始前一天不允许取消报名！！！'
        elif action == 'substitution':
            if is_full:
                tips = '替补成功'
                substitution_activity = BadmintonActivityDetails(join_weChat_id=request.user.id, activity_number_id=int(activity_id),
                                                                 is_substitution=True)
                substitution_activity.save()
            else:
                tips = '该活动未订满，请直接报名'
            logger.info(tips)
        elif action == 'cancel_substitution':
            tips = '取消替补成功'
            cancel_activity = BadmintonActivityDetails.objects.filter(activity_number_id=int(activity_id), join_weChat_id=request.user.id).delete()
        # context = {'activity': activityDetails, 'user_info': new_join_dic, "tips": tips, "activity_time": activity_time}
            logger.info(tips)
    if join_count >= limit_count:
        change_limit = BadmintonActivity.objects.get(activity_number=int(number))
        change_limit.is_full = 1
        change_limit.save()
    # page1 = paginator.page1(1)  # 第1页的page对象

    paginator = Paginator(new_join_dic, 10)  # 按照每页显示10条来计算
    page = request.GET.get('page', 1)  # 将来访问的url是这样的 http://127.0.0.1:8000/路径/?page=1
    currentPage = int(page)
    logger.info(new_join_dic)
    try:
        new_join_dic = paginator.page(page)
    except PageNotAnInteger:
        new_join_dic = paginator.page(1)
    except EmptyPage:
        new_join_dic = paginator.page(paginator.num_pages)
    return render(request, 'activity.html', locals())


@csrf_exempt
def page_not_found(request):
    response = render('404.html')
    return response


@csrf_exempt
def page_error(request):
    response = render('500.html')
    return response


@csrf_exempt
def my_api(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        weChat = request.POST.get('weChat', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.create_user(username=username, password=password, weChat=weChat)
            user.save()
        except Exception as e:
            logger.info(e)
            return HttpResponse("注册失败")
        return HttpResponse("注册成功")


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
        user = User.objects.create_user(username=username, password=password, weChat=weChat)
        user.save()
        # headers = self.get_success_headers(serializer.data)
        data = {'code': 200, 'msg': '注册成功', 'data': serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)


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


class MyJSONWebTokenAPIView(JSONWebTokenAPIView):
    """
    登录错误信息返回重写JSONWebTokenAPIView
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
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


def jwt_response_payload_handler(token, user=None, request=None):
    """为返回的结果添加用户相关信息"""
    return {
        "msg": "success",
        "status": 200,
        "data":{
            'token': token,
        'user_id': user.id,
        'username': user.username
                 }
    }


def jwt_response_payload_error_handler(serializer, request = None):
    return {
        "msg": "用户名或者密码错误",
        "status": 400,
        "errors": serializer.errors['non_field_errors'][0]
    }
  

class MyObtainJSONWebToken(ObtainJSONWebToken, MyJSONWebTokenAPIView):
    pass


class MyRefreshJSONWebToken(RefreshJSONWebToken, MyJSONWebTokenAPIView):
    pass


class MyVerifyJSONWebToken(VerifyJSONWebToken, MyJSONWebTokenAPIView):
    pass


obtain_jwt_token = MyObtainJSONWebToken.as_view()
refresh_jwt_token = MyRefreshJSONWebToken.as_view()
verify_jwt_token = MyVerifyJSONWebToken.as_view()
