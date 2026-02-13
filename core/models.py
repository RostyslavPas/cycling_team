import re

from django.db import models
from django.utils import timezone

WEEKDAY_CHOICES = [
    ("monday", "Понеділок"),
    ("tuesday", "Вівторок"),
    ("wednesday", "Середа"),
    ("thursday", "Четвер"),
    ("friday", "Пʼятниця"),
    ("saturday", "Субота"),
    ("sunday", "Неділя"),
]


class Training(models.Model):
    title = models.CharField(max_length=200)
    weekday = models.CharField(max_length=20, choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    start_location = models.CharField(max_length=200, default="Зупинка Авторинок")
    finish_location = models.CharField(max_length=200, default="Лісники (Макдональдс)")
    training_type = models.CharField(max_length=200)
    strava_embed_url = models.URLField(blank=True)
    has_auto_support = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "start_time"]

    def __str__(self):
        return f"{self.title} ({self.get_weekday_display()} {self.start_time})"

    @property
    def strava_route_id(self):
        if not self.strava_embed_url:
            return ""
        match = re.search(r"/routes/(\d+)", self.strava_embed_url)
        return match.group(1) if match else ""

    @property
    def strava_route_url(self):
        if self.strava_route_id:
            return f"https://www.strava.com/routes/{self.strava_route_id}"
        return self.strava_embed_url

    @property
    def strava_embed_src(self):
        if not self.strava_embed_url:
            return ""
        if "/embed" in self.strava_embed_url:
            return self.strava_embed_url
        if self.strava_route_id:
            return f"https://www.strava.com/routes/{self.strava_route_id}/embed"
        return self.strava_embed_url

    @property
    def strava_app_url(self):
        if self.strava_route_id:
            return f"strava://routes/{self.strava_route_id}"
        return ""


class TeamMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role_title = models.CharField(max_length=150)
    bio = models.CharField(max_length=300)
    photo = models.ImageField(upload_to="team", blank=True, null=True)
    instagram_url = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="sponsors", blank=True, null=True)
    url = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class TrainingSignup(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    training_date = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    comment = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.training}"


class AcademySignup(models.Model):
    first_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} - {self.phone}"
