from django.contrib import admin
from .models import MyUser, BadmintonActivity, BadmintonActivityDetails
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
import base64


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    def weChat(self, obj):
        return base64.b64decode(obj.all()).decode('utf8')
    list_display = ['username', 'weChat']
    list_per_page = 10
    # 新增用户时，在个人信息里添加'weChat'的信息录入
    # 将源码的UserAdmin.fieldsets转换成列表格式
    fieldsets = list(UserAdmin.fieldsets)
    # 重写UserAdmin的fieldsets，添加'weChat'的信息录入
    fieldsets[1] = (gettext_lazy('Personal info'),
                    {'fields':
                         ('first_name', 'last_name', 'weChat')})
    add_fieldsets = ((
                         None,
                         {'classes': ('wide',),
        'fields': ('username', 'weChat', 'password1', 'password2')}
        ),

    )


@admin.register(BadmintonActivity)
class BadmintonActivityAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['activity_number', 'activity_name', 'is_full', 'activity_place', 'activity_start_time', 'activity_end_time', 'is_alive', 'limit_count', 'is_cancel', 'is_operate', 'place_number']


@admin.register(BadmintonActivityDetails)
class BadmintonActivityDetailsAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['activity_number', 'join_weChat', 'is_substitution', 'operate_time']

