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
<<<<<<< HEAD:new_user/admin.py
    list_display = ['activity_number', 'activity_start_time', 'activity_end_time', 'is_alive']
=======
    list_display = ['activity_number', 'activity_name', 'activity_start_time', 'activity_end_time', 'is_alive']
>>>>>>> be3e2b019a706337e2f5d92ff18d71ee31c4b434:user/admin.py


@admin.register(BadmintonActivityDetails)
class BadmintonActivityDetailsAdmin(admin.ModelAdmin):
    list_display = ['activity_number', 'join_weChat']

#
# @admin.register(BadmintonActivityJoin)
# class BadmintonActivityJoinAdmin(admin.ModelAdmin):
#     list_display = ['activity_number', 'join_weChat']
