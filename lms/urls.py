from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='lms/login.html'), name='login'),
    path('logout_page/', views.logout_view, name='logout'),
    path('learner-dashboard/', views.learner_dashboard, name='learner_dashboard'),
    path('mentor-dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    path('role-selection/', views.role_selection, name='role_selection'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('start-mentoring/', views.start_mentoring, name='start_mentoring'),
    path('start_learning/', views.start_learning, name='start_learning'),
    path('get_timer/', views.get_timer, name='get_timer'),
    path('subjects/<str:subject_name>/', views.subject_page, name='subject_page'),

]
