from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from blog.models import Post


def posts_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    context = {
        'objects_list': posts,
        'title': 'Опубликованные статьи',
    }
    return render(request, 'blog/post/posts_list.html', context=context)


# def post_detail(request, year, month, day, post_object):
#     # post_object = get_object_or_404(Post.published, pk=pk)
#     post_object = get_object_or_404(Post, status=Post.Status.PUBLISHED)
#     context = {
#         'object': post_object,
#         'title': 'Детали поста',
#     }
#     return render(request, 'blog/post/post_detail.html',
#
#                   publish__year=year,
#                   publish__month=month,
#                   publish__day=day,
#                   slug=post_object,
#                   context=context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    context = {
        'title': 'Детали поста',
        'object': post,
    }
    return render(request,'blog/post/post_detail.html', context=context)
