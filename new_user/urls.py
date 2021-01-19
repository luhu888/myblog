from django.urls import path, include
# from django.conf.urls import handler404, handler500
from rest_framework import routers
# from rest_framework_jwt.views import obtain_jwt_token

from new_user import views
from new_user.views import JoinAPIViewSet

router = routers.DefaultRouter()
# router.register(r'register', RegisterViewSet)
# router.register('join', JoinAPIViewSet)

urlpatterns = [
    path('login.html', views.loginView, name='login'),  # name为别名，在html中指代这里
    # 为你的 URL 取名能使你在 Django 的任意地方唯一地引用它，尤其是在模板中。这个有用的特性允许你只改一个文件就能全局地修改某个 URL 模式。
    path('register.html', views.registerView, name='register'),
    path('setpassword.html', views.setpasswordView, name='setpassword'),
    path('logout.html', views.logoutView, name='logout'),
    path('activity/<int:number>.html', views.activityView, name='activity'),
    path('register_api', views.my_api, name='register_api'),
    path('api/login', views.obtain_jwt_token),
    # path('api/login', views.my_obtain_jwt_token),
    path('api/', include(router.urls)),
    path('api/register', views.RegisterAPIView.as_view()),
    path('api/join', views.JoinAPIViewSet.as_view())


]
#
# handler404 = views.page_not_found
# handler500 = views.page_error
