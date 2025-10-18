from django.urls import path

from users.apps import UsersConfig
from users.views import register_view, login_view, logout_view, profile_view

app_name = UsersConfig.name

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),

]

