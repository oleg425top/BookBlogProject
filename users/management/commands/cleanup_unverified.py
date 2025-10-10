from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import User

CODE_LIFETIME = timedelta(minutes=5)  # или 5, 10 — сколько нужно

class Command(BaseCommand):
    help = "Удаляет неподтвержденных пользователей с истекшим сроком кода"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_users = User.objects.filter(
            is_phone_verified=False,
            is_active=False,
            phone_confirmation_sent_at__lt=now - CODE_LIFETIME
        )

        count = expired_users.count()
        expired_users.delete()

        self.stdout.write(self.style.SUCCESS(f"Удалено {count} неподтвержденных пользователей"))
