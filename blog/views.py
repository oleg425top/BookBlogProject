from django.views.generic import ListView

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.forms import EmailPostForm
from blog.models import Post
from blog.services import send_email


# def posts_list(request):
#     post_list = Post.published.all()
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     context = {
#         'objects_list': posts,
#         'title': 'Опубликованные статьи',
#     }
#     return render(request, 'blog/post/posts_list.html', context=context)

class PostListView(ListView):
    queryset = Post.published.all()
    # context_object_name = 'objects_list'
    paginate_by = 3
    template_name = 'blog/post/posts_list.html'


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
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month,
                             publish__day=day)
    context = {
        'post':post,
        'title': 'Детали поста',
        'object': post,
    }
    return render(request, 'blog/post/post_detail.html', context=context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_email(
                post=post,
                recipient_email=cd['to'],
                cd=cd['name'],
                comments=cd['comments'],
                request=request,
            )
            sent = True
    else:
        form = EmailPostForm()
    context = {
            'post': post,
            'form': form,
            'sent':sent,
        }
    return render(request, 'blog/post/share.html', context=context)
