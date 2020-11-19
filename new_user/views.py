import base64

from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from new_user.models import MyUser as User  # 扩展user后使用新的MyUser
from new_user.models import BadmintonActivity, BadmintonActivityDetails, MyUser
from django.contrib.auth import login, logout, authenticate
import logging
# from django import forms


logger = logging.getLogger('django')

week_change = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六一', '7': '日'}

# class UserForm(forms.Form):
#     name = forms.CharField(min_length=4, label='用户名', required=True, help_text='必填')   # 必须用required
#     pwd = forms.CharField(min_length=4, label='密码', required=True, help_text='必填')
#     weChat = forms.CharField(min_length=4, label='微信号', required=True, help_text='必填')


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
                    login(request, user)
                    return redirect('/')
                else:
                    tips = '账号密码错误，请重新输入'
            else:
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

        password = request.POST.get('password', '')
        if User.objects.filter(username=username) or User.objects.filter(weChat=weChat):
            tips = '用户已存在'
        elif username == '' or weChat1 == '' or password == '':
            tips = '请将注册信息填写完整'
        else:
            user = User.objects.create_user(username=username, password=password, weChat=weChat)
            user.save()
            tips = '注册成功，请登录'
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


def activityView(request, number):
    username = request.user.username
    activityDetails = BadmintonActivityDetails.objects.filter(activity_number_id=int(number))
    join_dic = {}
    new_join_dic = {}
    is_join = BadmintonActivityDetails.objects.filter(activity_number_id=int(number), join_weChat_id=request.user.id, is_substitution=False)
    is_substitution = BadmintonActivityDetails.objects.filter(activity_number_id=int(number), join_weChat_id=request.user.id, is_substitution=True)
    is_full = BadmintonActivity.objects.filter(id=int(number)).values_list('is_full')[0][0]
    action = request.POST.get("action", '')
    join_dic = dict(BadmintonActivityDetails.objects.filter(activity_number_id=int(number)).values_list('join_weChat', 'is_substitution'))
    activity_end_time = BadmintonActivity.objects.get(activity_number=int(number)).activity_end_time.strftime('%H:%M')
    activity_start_time = BadmintonActivity.objects.get(activity_number=int(number)).activity_start_time.strftime("%Y-%m-%d %H:%M")
    activity_week = BadmintonActivity.objects.get(activity_number=int(number)).activity_start_time.isoweekday()
    activity_time = str(activity_start_time) + '-' + str(activity_end_time) + ' 周' + week_change[str(activity_week)]
    activity_place = str(BadmintonActivity.objects.get(activity_number=int(number)).activity_place)
    join_count = str(BadmintonActivityDetails.objects.filter(activity_number_id=int(number)).count())
    surplus = str(12 - int(join_count))
    logger.info(activity_place)
    for i in activityDetails:
        for j in join_dic.keys():
            new_join_dic[base64.b64decode(MyUser.objects.get(id=j).weChat).decode('utf8')] = join_dic[j]
    if request.method == 'POST':
        if bool(is_join) and action == 'join':
            tips = '您已成功报名，请勿重复报名'
            # logger.info(tips)
        elif action == 'join':
            tips = '报名成功'
            join_person = BadmintonActivityDetails(join_weChat_id=request.user.id, activity_number_id=int(number))
            join_person.save()
        elif action == 'cancel':
            tips = '取消报名成功'
            cancel_activity = BadmintonActivityDetails.objects.filter(activity_number_id=int(number), join_weChat_id=request.user.id).delete()
            # logger.info(txt1)
        elif action == 'substitution':
            tips = '替补成功'
            substitution_activity = BadmintonActivityDetails(join_weChat_id=request.user.id, activity_number_id=int(number),
                                                             is_substitution=True)
            substitution_activity.save()
            logger.info(tips)
        elif action == 'cancel_substitution':
            tips = '取消替补成功'
            cancel_activity = BadmintonActivityDetails.objects.filter(activity_number_id=int(number), join_weChat_id=request.user.id).delete()
        context = {'activity': activityDetails, 'user_info': new_join_dic, "tips": tips, "activity_time": activity_time}
        logger.info(tips)
    logger.info(new_join_dic)
    return render(request, 'activity.html', locals())


@csrf_exempt
def my_api(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        weChat = request.POST.get('weChat', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.create_user(username=username, password=password, weChat=base64.b64encode(weChat.encode('utf8')))
            user.save()
        except Exception as e:
            print(e)
            return HttpResponse("注册失败")
        return HttpResponse("注册成功")