from django.urls import path, include
from rest_framework import routers

from myAPI import views

router = routers.DefaultRouter()
# router.register(r'register', RegisterViewSet)
# router.register('join', JoinAPIViewSet)

urlpatterns = [
    path('api/join', views.JoinAPIViewSet.as_view()),
    path('api/login', views.obtain_jwt_token),
    path('api/', include(router.urls)),
    path('api/register', views.RegisterAPIView.as_view()),
    path('api/activityDetail/', views.GetJoinListView.as_view()),
    path('api/activity/', views.ActivityListView.as_view()),
    path('api/substitution', views.SubstitutionAPIViewSet.as_view()),
    path('api/cancelJoin', views.CancelAPIView.as_view()),
]
#
# handler404 = views.page_not_found
# handler500 = views.page_error
