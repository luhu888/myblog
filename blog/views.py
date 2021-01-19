from django.http import HttpResponse
from django.shortcuts import render
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from new_user.models import BadmintonActivity, BadmintonActivityDetails, MyUser as User
from rest_framework import routers, serializers, viewsets
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from blog.models import Category
from blog.serializers import CategorySerializer
from rest_framework.response import Response

logger = logging.getLogger('django')


@csrf_exempt
def index(request):
    username = request.user.username
    activity = BadmintonActivity.objects.filter(is_alive=False)
    context = {
        'activity': activity,
    }
    return render(request, 'index.html', locals())


@csrf_exempt
def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


class JSONResponse(HttpResponse):
    """
    将数据渲染成json返回
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def category_list(request):
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    # 序列化类
    serializer_class = CategorySerializer
    # 查询集和结果集
    queryset = Category.objects.all()
    # 用户验证
    # authentication_classes = (JSONWebTokenAuthentication, )  # SessionAuthentication
    # permission_classes = [IsAuthenticated,]   # 指定访问该接口需要什么权限 AllowAny,IsAuthenticated
    def list(self, request, *args, **kwargs):
        """
        自定义接口返回格式
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().list(request, *args, **kwargs)
        return Response({'code': 200, 'msg': '成功', 'data':response.data})