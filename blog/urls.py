from django.urls import path

from blog.apps import BlogConfig
from blog.views import post_detail, PostListView, post_share, post_comment, posts_list, index_view

app_name = BlogConfig.name

urlpatterns = [
    path('', index_view, name='index'),
    path('blog/', posts_list, name='posts_list'),
    # path('blog/', PostListView.as_view(), name='posts_list'),
    path('blog/tag/<slug:tag_slug>/', posts_list, name='posts_list_by_tag'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('blog/<int:post_id>/share/', post_share, name='post_share'),
    path('blog/<int:post_id>/comment/', post_comment, name='post_comment'),
]
