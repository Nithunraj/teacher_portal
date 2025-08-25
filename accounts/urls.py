from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register_user/', views.register_user, name='register_user'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('add_student/',views.add_student, name='add_student'),
    path('update_student/<int:pk>/',views.update_student, name='update_student'),
    path('delete_student/<int:pk>/',views.delete_student, name='delete_student'),
    path('logs/',views.logs, name='logs'),
]
