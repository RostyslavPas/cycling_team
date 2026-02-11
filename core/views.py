from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from .forms import TrainingSignupForm
from .models import Training, TeamMember, Sponsor, TrainingSignup


def landing_page(request):
    trainings = Training.objects.filter(is_active=True).order_by("sort_order", "start_time")
    members = TeamMember.objects.filter(is_active=True).order_by("sort_order", "last_name")
    sponsors = Sponsor.objects.filter(is_active=True).order_by("sort_order", "name")

    context = {
        "page": "landing",
        "trainings": trainings,
        "members": members,
        "sponsors": sponsors,
        "today": date.today(),
    }
    return render(request, "site.html", context)


def privacy_policy(request):
    context = {
        "page": "privacy",
        "page_title": "Privacy Policy",
        "page_body": [
            "We collect only the information you submit in the training signup form and basic request metadata.",
            "We use this data solely to coordinate training sessions and team communication.",
            "We do not sell or share your information with third parties.",
            "You can request deletion of your data by contacting the team administrator.",
        ],
    }
    return render(request, "site.html", context)


def terms_of_use(request):
    context = {
        "page": "terms",
        "page_title": "Terms of Use",
        "page_body": [
            "Training participation is voluntary and at your own risk.",
            "You agree to follow the team safety rules and local traffic regulations.",
            "Schedules may change due to weather or operational needs.",
        ],
    }
    return render(request, "site.html", context)


@staff_member_required
def training_day_detail(request, weekday, training_date):
    training = get_object_or_404(Training, weekday=weekday)
    parsed_date = parse_date(training_date)
    if not parsed_date:
        raise Http404("Invalid date")

    signups = TrainingSignup.objects.filter(
        training=training, training_date=parsed_date
    ).order_by("created_at")

    context = {
        "page": "training_day",
        "training": training,
        "training_date": parsed_date,
        "signups": signups,
    }
    return render(request, "site.html", context)


def _client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@require_POST
def api_signup(request):
    form = TrainingSignupForm(request.POST)
    if form.is_valid():
        signup = form.save(commit=False)
        signup.ip_address = _client_ip(request)
        signup.user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
        signup.save()
        return JsonResponse(
            {"success": True, "message": "Дякуємо! Ми звʼяжемось із вами найближчим часом."}
        )

    return JsonResponse({"success": False, "errors": form.errors}, status=400)
