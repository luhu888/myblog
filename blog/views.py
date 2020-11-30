from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from new_user.models import BadmintonActivity, BadmintonActivityDetails
from blog.models import Article
import logging
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from blog.models import Category
# from blog.serializers import CategorySerializer


logger = logging.getLogger('django')


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


@csrf_exempt
def index(request):
    username = request.user.username
    activity = BadmintonActivity.objects.filter(is_alive=False)
    # for i in activity:
        # logger.info(i.is_full)
    context = {
        'activity': activity,
    }
    return render(request, 'index.html', locals())


@csrf_exempt
def page_not_found(request):
    return render_to_response(request, '404.html')


def page_error(request):
    return render_to_response(request, '500.html')


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# @csrf_exempt
# def category_list(request):
#     """
#     列出所有的code snippet，或创建一个新的snippet。
#     """
#     if request.method == 'GET':
#         category = Category.objects.all()
#         serializer = CategorySerializer(category, many=True)
#         return JSONResponse(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = CategorySerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=201)
#         return JSONResponse(serializer.errors, status=400)