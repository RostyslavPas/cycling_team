from datetime import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Training, Sponsor, TeamMember


class Command(BaseCommand):
    help = "Seed initial trainings and sponsors."

    def _media_file_exists(self, relative_path):
        return (Path(settings.MEDIA_ROOT) / relative_path).exists()

    def handle(self, *args, **options):
        trainings = [
            {
                "title": "Tuesday Training",
                "weekday": "tuesday",
                "start_time": time(7, 0),
                "start_location": "Зупинка Авторинок",
                "finish_location": "Лісники (Макдональдс)",
                "training_type": "Інтервальне тренування",
                "strava_embed_url": "https://www.strava.com/routes/3272635248872583956/embed",
                "has_auto_support": True,
                "is_active": True,
                "sort_order": 1,
            },
            {
                "title": "Thursday Training",
                "weekday": "thursday",
                "start_time": time(7, 0),
                "start_location": "Зупинка Авторинок",
                "finish_location": "Лісники (Макдональдс)",
                "training_type": "Гірки",
                "strava_embed_url": "https://www.strava.com/routes/3390740289357252534/embed",
                "has_auto_support": True,
                "is_active": True,
                "sort_order": 2,
            },
            {
                "title": "Saturday Training",
                "weekday": "saturday",
                "start_time": time(8, 0),
                "start_location": "Зупинка Авторинок",
                "finish_location": "Лісники (Макдональдс)",
                "training_type": "Обʼємне тренування",
                "strava_embed_url": "https://www.strava.com/routes/3390990324918245792/embed",
                "has_auto_support": True,
                "is_active": True,
                "sort_order": 3,
            },
        ]

        for data in trainings:
            Training.objects.update_or_create(
                title=data["title"],
                defaults=data,
            )

        sponsors = [
            {
                "name": "Creative States",
                "sort_order": 1,
                "is_active": True,
                "logo_path": "sponsors/creative_states_logos.png",
            },
            {
                "name": "Сучасні Безпілотні технології",
                "sort_order": 2,
                "is_active": True,
                "logo_path": "sponsors/sbt.svg",
            },
            {
                "name": "Sportunite",
                "sort_order": 3,
                "is_active": True,
                "logo_path": "sponsors/sportunite.png",
            },
        ]

        for data in sponsors:
            logo_path = data.pop("logo_path", "")
            defaults = data.copy()
            if logo_path and self._media_file_exists(logo_path):
                defaults["logo"] = logo_path
            Sponsor.objects.update_or_create(
                name=data["name"],
                defaults=defaults,
            )

        members = [
            {
                "first_name": "Анатолій",
                "last_name": "Зінченко",
                "role_title": "Founder & Team Captain",
                "bio": "Темп і дисципліна на кожному тренуванні.",
                "instagram_url": "",
                "sort_order": 1,
                "is_active": True,
                "photo_path": "team/tolik.png",
            },
            {
                "first_name": "Олександр",
                "last_name": "Матвієнко",
                "role_title": "Climber",
                "bio": "Висока витривалість і контроль темпу.",
                "instagram_url": "",
                "sort_order": 6,
                "is_active": True,
                "photo_path": "team/sasha.png",
            },
            {
                "first_name": "Леонід",
                "last_name": "Полупан",
                "role_title": "Endurance Specialist",
                "bio": "Стабільна витривалість і командна підтримка.",
                "instagram_url": "",
                "sort_order": 3,
                "is_active": True,
                "photo_path": "team/leonid.png",
            },
            {
                "first_name": "Олександр",
                "last_name": "Грюканов",
                "role_title": "Climber",
                "bio": "Потужний темповий профіль із фокусом на довгі дистанції.",
                "instagram_url": "",
                "sort_order": 4,
                "is_active": True,
                "photo_path": "team/sasha_gr.png",
            },
            {
                "first_name": "Ростислав",
                "last_name": "Пась",
                "role_title": "Founder & Creative Director",
                "bio": "Стратегія команди, візуальна ідентичність і креативний розвиток.",
                "instagram_url": "",
                "sort_order": 5,
                "is_active": True,
                "photo_path": "team/ros.png",
            },
            {
                "first_name": "Юрій",
                "last_name": "Голик",
                "role_title": "Founder & Team Director",
                "bio": "Засновник, управління і розвиток команди.",
                "instagram_url": "",
                "sort_order": 2,
                "is_active": True,
                "photo_path": "team/yuriy.png",
            },
        ]

        for data in members:
            photo_path = data.pop("photo_path")
            defaults = data.copy()
            if self._media_file_exists(photo_path):
                defaults["photo"] = photo_path
            TeamMember.objects.update_or_create(
                sort_order=data["sort_order"],
                defaults=defaults,
            )

        self.stdout.write(self.style.SUCCESS("Initial data seeded."))
