from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.web_login, name='login'),
    path('logout/', views.web_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('submit/', views.report_leak, name='submit-leak'),
    path('my-reports/', views.my_reports, name='my-reports'),
    path('adm/dashboard/', views.admin_dash, name='admin-dashboard'),
    path('tm/dashboard/', views.team_dash, name='team-dashboard'),
    path('pb/dashboard/', views.public_dash, name='public-dashboard'),
    path('mng/assign/<int:report_id>/', views.assign_report, name='assign-report'),
    path('mng/resolve/<int:report_id>/', views.resolve, name='resolve'),
]