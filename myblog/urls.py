"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path


from blog import views
from django.views.static import serve
# 导入静态文件模块
from django.conf import settings
# 导入配置文件里的文件上传配置
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),  # 添加DjangoUeditor的URL
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),    # 增加此行
    path('', views.index),  # 里面留空，代表首页
    path('new_user/', include('new_user.urls'))
    # path('articles/<int:year>/', views.year_archive, name='news-year-archive'),
    # path('news/', views.news),  # news
    # path('bbs/', views.bbs),  # bbs
]
