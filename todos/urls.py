from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Redirect to signup/login first
    path('todos/', views.todo_list, name='todo_list'),
    path('add/', views.todo_create, name='todo_create'),
    path('edit/<int:pk>/', views.todo_edit, name='todo_edit'),
    path('delete/<int:pk>/', views.todo_delete, name='todo_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('export/excel/', views.export_todos_excel, name='export_excel'),
     
]
