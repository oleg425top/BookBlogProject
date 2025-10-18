from django import template

register = template.Library()


@register.filter()
def user_media(val):
    if val:
        return f'/{val}'
    return '/static/img/no_avatar.jpg'
