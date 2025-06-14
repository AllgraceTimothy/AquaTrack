from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'leak-reports', views.LeakReportViewSet, basename='leakreport')

urlpatterns = [
    path('auth/signup/', views.app_signup),
    path('auth/login/', views.app_login),
    path('', include(router.urls)),
]
