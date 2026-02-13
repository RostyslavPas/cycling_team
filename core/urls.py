from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("academy/", views.academy_page, name="academy"),
    path("privacy/", views.privacy_policy, name="privacy"),
    path("terms/", views.terms_of_use, name="terms"),
    path("trainings/<slug:weekday>/<str:training_date>/", views.training_day_detail, name="training_day"),
    path("api/signup/", views.api_signup, name="api_signup"),
    path("api/academy-signup/", views.api_academy_signup, name="api_academy_signup"),
]
