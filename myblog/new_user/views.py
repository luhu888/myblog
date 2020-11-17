from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from new_user.models import MyUser as User  # 扩展user后使用新的MyUser
from new_user.models import BadmintonActivity, BadmintonActivityDetails, MyUser
from django.contrib.auth import login, logout, authenticate
import logging
from django import forms
from django.forms import widgets


class UserForm(forms.Form):
    name = forms.CharField(min_length=4, label='用户名', required=True, help_text='必填')   # 必须用required
    pwd = forms.CharField(min_length=4, label='密码', required=True, help_text='必填')
    weChat = forms.CharField(min_length=4, label='微信号', required=True, help_text='必填')


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
        form = UserForm(request.POST)  # form表单的name属性值应该与forms组件字段名称一致
        username = request.POST.get('username', '')
        weChat = request.POST.get('weChat', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username):
            tips = '用户已存在'
        elif username == '' or weChat == '' or password == '':
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
    # BadmintonActivity.objects.values(fk=int(number))
    user_info = []
    for i in activityDetails:
        # key = BadmintonActivity.objects.get(id=int(number))
        value = MyUser.objects.filter(id=i.join_weChat_id).values_list('weChat')[0][0]
        # value = 'rr'
        user_info.append(value)
    context = {
        'activity': activityDetails,
        'user_info': user_info
    }
    return render(request, 'activity.html', locals())
