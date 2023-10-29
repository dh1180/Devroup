from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('', views.user_profile, name='user_profile'),
    path('change_username/', views.change_username, name='change_username'),

]
