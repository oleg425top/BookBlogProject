from django.urls import path

from users.apps import UsersConfig
from users.views import register, profile, logout, login_view

app_name = UsersConfig.name

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),

]

