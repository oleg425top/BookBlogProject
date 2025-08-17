from django.urls import path

from blog.apps import BlogConfig
from blog.views import post_detail, PostListView, post_share

app_name = BlogConfig.name

urlpatterns = [
    # path('', posts_list, name='posts_list'),
    path('', PostListView.as_view(), name='posts_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
]
