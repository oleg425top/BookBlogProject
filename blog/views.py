from re import search

from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag

from blog.forms import EmailPostForm, CommentForm, PostForm, SearchForm
from blog.models import Post
from blog.services import send_email
from blog.utils import slug_generator


def index_view(request):
    posts = Post.published.all()[:3]
    context = {
        'title':'Home: главная',
        'posts':posts,

    }
    return render(request, 'blog/post/index.html', context=context)


def posts_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'tag':tag,
        'title': 'Опубликованные статьи',
    }
    return render(request, 'blog/post/posts_list.html', context=context)

class PostListView(ListView):
    queryset = Post.published.all()
    # context_object_name = 'objects_list'
    paginate_by = 2
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

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if not post.slug:
                post.slug = slug_generator(post.title)
            post.save()
            return HttpResponseRedirect(reverse('blog:posts_list'))
    else:
        form = PostForm()
        return render(request, 'blog/post/post_create.html', {'title':'Создание поста', 'form': form})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    context = {
        'post':post,
        'comments':comments,
        'title': 'Детали поста',
        'object': post,
        'form':form,
        'similar_posts':similar_posts,
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

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
            'post': post,
            'form': form,
            'comment':comment,
        }
    return render(request, 'blog/post/comment.html', context=context)


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:posts_list')
    context = {
            'post': post,
            'title': 'Удалить пост',
        }
    return render(request, 'blog/post/post_delete.html', context=context)

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + \
                            SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query),
            ).filter(rank__gte=0.3).order_by('-rank')
    context = {
                'title':'Posts Search',
                'form':form,
                'query':query,
                'results':results
            }
    return render(request, 'blog/post/search.html', context=context)