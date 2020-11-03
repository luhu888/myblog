from django.contrib import admin
from .models import MyUser, BadmintonActivity, BadmintonActivityDetails
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ['username', 'weChat']
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
    list_display = ['activity_number', 'activity_name', 'activity_time', 'is_alive']


@admin.register(BadmintonActivityDetails)
class BadmintonActivityDetailsAdmin(admin.ModelAdmin):
    list_display = ['activity_name', 'join_weChat', 'is_alive']

