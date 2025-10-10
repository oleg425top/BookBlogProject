from django.core.management.base import BaseCommand
from django.conf import settings
import psycopg2
from psycopg2 import sql


class Command(BaseCommand):
    help = "Создает базу данных PostgreSQL, если она еще не существует"

    def handle(self, *args, **options):
        db_settings = settings.DATABASES["default"]

        db_name = db_settings["NAME"]
        db_user = db_settings["USER"]
        db_password = db_settings["PASSWORD"]
        db_host = db_settings["HOST"]
        db_port = db_settings.get("PORT", "5432")

        # Подключаемся к postgres (системная база, всегда есть)
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Проверяем, существует ли база
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            self.stdout.write(self.style.SUCCESS(f"База данных '{db_name}' успешно создана"))
        else:
            self.stdout.write(self.style.WARNING(f"База данных '{db_name}' уже существует"))

        cur.close()
        conn.close()
