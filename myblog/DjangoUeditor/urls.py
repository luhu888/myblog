# coding:utf-8
from django import VERSION
from django.conf import settings
from django.urls import re_path, include
from django.views.static import serve

from .widgets import UEditorWidget, AdminUEditorWidget
from .views import get_ueditor_controller
from django.conf.urls import url

urlpatterns = [
    url(r'^controller/$', get_ueditor_controller),
]
