from django.conf.urls import url
from django.urls import path, include
from api.routers import router
from . import views

app_name = 'sn'
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    path('api/', views.BaseCreateView.as_view(), name='base'),
    path('api/analytics/', views.AnalyticsCreateView.as_view(), name='analytics'),
    path('api/user_activity/', views.UserActivityCreateView.as_view(), name='user_activity'),
]
