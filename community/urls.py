from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/create', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('profile/', views.change_username, name='change_username'),
    
]
