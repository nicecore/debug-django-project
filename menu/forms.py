from django import forms
from .models import Menu
from django.forms.widgets import SelectDateWidget
from django.utils import timezone


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
            'expiration_date'
        ]

        widgets = {
            'expiration_date': SelectDateWidget()
        }

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date and expiration_date <= timezone.now().date():
            raise forms.ValidationError(
                "The expiration date cannot be before the created date.")
        return expiration_date
