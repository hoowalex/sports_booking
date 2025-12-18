from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Головна сторінка
    path('', views.index, name='index'),

    # Робота з тренуваннями
    path('trainings/', views.training_list, name='trainings'),
    path('trainings/create/', views.create_training, name='create_training'),
    path('trainings/delete/<int:training_id>/', views.delete_training, name='delete_training'),
    path('trainings/join/<int:training_id>/', views.join_training, name='join_training'),
    path('trainings/leave/<int:training_id>/', views.leave_training, name='leave_training'),

    # Профіль користувача
    path('profile/', views.profile, name='profile'),

    # Авторизація (вхід/вихід)
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
]