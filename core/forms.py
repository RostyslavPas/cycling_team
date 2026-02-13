from django import forms
from .models import Training, TrainingSignup, AcademySignup


class TrainingSignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["training"].queryset = Training.objects.filter(is_active=True)

    class Meta:
        model = TrainingSignup
        fields = [
            "training",
            "training_date",
            "first_name",
            "last_name",
            "phone",
            "comment",
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not phone:
            raise forms.ValidationError("Phone is required.")
        return phone


class AcademySignupForm(forms.ModelForm):
    class Meta:
        model = AcademySignup
        fields = ["first_name", "phone", "consent"]

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip()
        if not first_name:
            raise forms.ValidationError("Вкажіть імʼя.")
        return first_name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not phone:
            raise forms.ValidationError("Вкажіть номер телефону.")
        return phone

    def clean_consent(self):
        consent = self.cleaned_data.get("consent")
        if not consent:
            raise forms.ValidationError("Потрібно підтвердити згоду на обробку даних.")
        return consent
