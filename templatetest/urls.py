from django.urls import path
from rest_framework import routers

from templatetest import views

router = routers.DefaultRouter()
# router.register(r'register', RegisterViewSet)
# router.register('join', JoinAPIViewSet)

urlpatterns = [
    path('base/', views.base),
    path('menu1/', views.menu1),
    path('menu2/', views.menu2),
    path('menu3/', views.safe_value),

]
#
# handler404 = views.page_not_found
# handler500 = views.page_error
