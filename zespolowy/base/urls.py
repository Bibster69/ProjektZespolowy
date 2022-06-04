from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.list_tasks.as_view(), name='task_list'),
    path('register/', views.register_view.as_view(), name='register'),
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('task_detail/<int:pk>/', views.task_detail.as_view(), name='task_detail'),
    path('task_create/', views.task_create.as_view(), name='task_create'),
    path('task_update/<int:pk>', views.task_update.as_view(), name='task_update'),
    path('task_confirm_delete/<int:pk>', views.task_delete.as_view(), name='task_delete')
]
