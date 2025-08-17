from django.conf import settings
from django.core.mail import send_mail


def send_email(post, recipient_email, cd, comments, request):
    post_url = request.build_absolute_uri(post.get_absolute_url())
    subject = f"{cd} recommends you read {post.title}"
    message = f"Read {post.title} at {post_url}\n\n{cd}'s comments: {comments}"
    send_mail(
        subject=subject,
        message=message,
        from_email='oleg1986mail@yandex.ru',
        recipient_list=[recipient_email],
    )

