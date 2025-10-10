from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Создаёт суперпользователя (админа)"

    def handle(self, *args, **options):
        if not User.objects.filter(email="oleg1986mail@yandex.ru").exists():
            User.objects.create_superuser(
                email="oleg1986mail@yandex.ru",
                password="olegevgeniyseon",
                first_name="Admin",
                role="admin",
                last_name="User",
                phone="+79999999999",
                is_verified=True,
            )
            self.stdout.write(self.style.SUCCESS("Суперпользователь создан!"))
        else:
            self.stdout.write(self.style.WARNING("Суперпользователь уже существует."))
