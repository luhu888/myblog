from django.http import HttpResponse


# 添加一个函数
from django.shortcuts import render
from new_user.models import BadmintonActivity, BadmintonActivityDetails
from blog.models import Article


def index1(request):
    # 添加两个变量，并给它们赋值
    sitename = 'Django中文网'
    url = 'www.django.cn'
    # 把两个变量封装到上下文里
    list = [
        '开发前的准备',
        '项目需求分析',
        '数据库设计分析',
        '创建项目',
        '基础配置',
        '欢迎页面',
        '创建数据库模型',
    ]
    mydict = {
        'name': '吴秀峰',
        'qq': '445813',
        'wx': 'vipdjango',
        'email': '445813@qq.com',
        'Q群': '10218442',
    }
    context = {
        'sitename': sitename,
        'url': url,
        'list': list,
        'mydict': mydict,
    }
    # 把上下文传递到模板里
    return render(request, 'index1.html', context)


def index(request):
    username = request.user.username
    activity = BadmintonActivity.objects.filter(is_alive=False)
    context = {
        'activity': activity,
    }
    return render(request, 'index.html', locals())

