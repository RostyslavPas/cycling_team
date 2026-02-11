from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Training",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                (
                    "weekday",
                    models.CharField(
                        choices=[
                            ("monday", "Понеділок"),
                            ("tuesday", "Вівторок"),
                            ("wednesday", "Середа"),
                            ("thursday", "Четвер"),
                            ("friday", "Пʼятниця"),
                            ("saturday", "Субота"),
                            ("sunday", "Неділя"),
                        ],
                        max_length=20,
                    ),
                ),
                ("start_time", models.TimeField()),
                ("start_location", models.CharField(default="Зупинка Авторинок", max_length=200)),
                ("finish_location", models.CharField(default="Лісники (Макдональдс)", max_length=200)),
                ("training_type", models.CharField(max_length=200)),
                ("strava_embed_url", models.URLField(blank=True)),
                ("has_auto_support", models.BooleanField(default=True)),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["sort_order", "start_time"]},
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("role_title", models.CharField(max_length=150)),
                ("bio", models.CharField(max_length=300)),
                ("photo", models.ImageField(blank=True, null=True, upload_to="team")),
                ("instagram_url", models.URLField(blank=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["sort_order", "last_name"]},
        ),
        migrations.CreateModel(
            name="Sponsor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="sponsors")),
                ("url", models.URLField(blank=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["sort_order", "name"]},
        ),
        migrations.CreateModel(
            name="TrainingSignup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("training_date", models.DateField()),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=50)),
                ("comment", models.CharField(blank=True, max_length=300)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
                (
                    "training",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.training"),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
