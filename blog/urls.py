from django.urls import path, include
from rest_framework import routers

from blog.views import UserViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'category', CategoryViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]
