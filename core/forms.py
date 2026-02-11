from django import forms
from .models import Training, TrainingSignup


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
