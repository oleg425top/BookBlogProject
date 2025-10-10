from django.contrib import admin

from blog.models import Post, Comment


# admin.site.register(Post)

class PostTabAdmin(admin.TabularInline):
    """Интерфейс для редактирования корзины в контексте родительской модели."""
    model = Post
    fields = "title", "publish", "created"
    search_fields = "title", "publish", "created"
    readonly_fields = ("created",)
    extra = 1

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ['title', 'body']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
