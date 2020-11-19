from django.urls import path
from . import views
urlpatterns = [
    path('login.html', views.loginView, name='login'),  # name为别名，在html中指代这里
    # 为你的 URL 取名能使你在 Django 的任意地方唯一地引用它，尤其是在模板中。这个有用的特性允许你只改一个文件就能全局地修改某个 URL 模式。
    path('register.html', views.registerView, name='register'),
    path('setpassword.html', views.setpasswordView, name='setpassword'),
    path('logout.html', views.logoutView, name='logout'),
    path('activity/<int:number>.html', views.activityView, name='activity'),
    path('register_api', views.my_api, name='register_api')
]