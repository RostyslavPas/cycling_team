import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html

from .models import Training, TeamMember, Sponsor, TrainingSignup, AcademySignup


def export_signups_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=training_signups.csv"
    writer = csv.writer(response)
    writer.writerow(
        [
            "Training",
            "Weekday",
            "Training Date",
            "First Name",
            "Last Name",
            "Phone",
            "Comment",
            "Created At",
            "IP Address",
            "User Agent",
        ]
    )
    for signup in queryset.select_related("training"):
        writer.writerow(
            [
                signup.training.title,
                signup.training.weekday,
                signup.training_date,
                signup.first_name,
                signup.last_name,
                signup.phone,
                signup.comment,
                signup.created_at,
                signup.ip_address,
                signup.user_agent,
            ]
        )
    return response


export_signups_csv.short_description = "Export selected signups to CSV"


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "weekday",
        "start_time",
        "start_location",
        "training_type",
        "has_auto_support",
        "is_active",
        "sort_order",
    )
    list_filter = ("weekday", "is_active", "has_auto_support")
    search_fields = ("title", "start_location", "finish_location", "training_type")
    ordering = ("sort_order", "weekday", "start_time")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "photo_preview",
        "first_name",
        "last_name",
        "role_title",
        "is_active",
        "sort_order",
    )
    list_filter = ("is_active",)
    search_fields = ("first_name", "last_name", "role_title", "bio")
    ordering = ("sort_order", "last_name")

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:50%;" />', obj.photo.url)
        return "—"

    photo_preview.short_description = "Photo"


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("logo_preview", "name", "url", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("sort_order", "name")

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:30px;object-fit:contain;" />', obj.logo.url)
        return "—"

    logo_preview.short_description = "Logo"


@admin.register(TrainingSignup)
class TrainingSignupAdmin(admin.ModelAdmin):
    list_display = (
        "training",
        "training_date",
        "first_name",
        "last_name",
        "phone",
        "created_at",
    )
    list_filter = ("training", "training_date", "created_at")
    search_fields = ("first_name", "last_name", "phone", "comment")
    ordering = ("-created_at",)
    actions = [export_signups_csv]


@admin.register(AcademySignup)
class AcademySignupAdmin(admin.ModelAdmin):
    list_display = ("first_name", "phone", "consent", "created_at")
    list_filter = ("consent", "created_at")
    search_fields = ("first_name", "phone")
    ordering = ("-created_at",)
