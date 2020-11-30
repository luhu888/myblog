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
from django.views.static import serve
from django.conf.urls import handler404, handler500
# 导入静态文件模块
from blog import views
from django.conf import settings
from django.views.generic.base import RedirectView
# 导入配置文件里的文件上传配置
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),  # 添加DjangoUeditor的URL
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),    # 增加此行
    path('', views.index),  # 里面留空，代表首页
    path('new_user/', include('new_user.urls')),
    re_path(r'^favicon.ico$', RedirectView.as_view(url=r'static/images/favicon.ico'))
    # path('articles/<int:year>/', views.year_archive, name='news-year-archive'),
    # path('news/', views.news),  # news
    # path('bbs/', views.bbs),  # bbs
]
handler404 = views.page_not_found
handler500 = views.page_error
admin.site.site_header = "小羽毛报名系统"
admin.site.site_title = "小羽毛报名系统"
admin.site.index_title = "欢迎进入小羽毛报名系统"
