from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
import base64

from myAPI.models import MyUser, APIActivity, APIActivityRelated


@admin.register(APIActivity)
class BadmintonActivityAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['activity_number', 'activity_name', 'is_full', 'activity_place', 'activity_start_time', 'activity_end_time', 'is_alive', 'limit_count', 'is_cancel', 'is_operate', 'place_number']


@admin.register(APIActivityRelated)
class BadmintonActivityDetailsAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['activity_number', 'joiner', 'is_substitution', 'operate_time']

