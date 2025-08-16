from django.urls import path

from blog.apps import BlogConfig
from blog.views import post_detail, posts_list

app_name = BlogConfig.name

urlpatterns = [
    path('', posts_list, name='posts_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
]
