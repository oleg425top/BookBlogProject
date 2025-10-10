from django.contrib import admin

from blog.admin import PostTabAdmin
from users.models import User

# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'is_active')
    list_filter = ('last_name',)

    inlines = [PostTabAdmin]
