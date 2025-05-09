from django import forms
from .models import UserData
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Passwort', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Passwort wiederholen', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserData
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise ValidationError("Die Passwörter stimmen nicht überein.")
        
        return cleaned_data