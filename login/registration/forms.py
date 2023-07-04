from django import forms
from django.contrib.auth.models import User
from django.contrib. auth.forms import UserCreationForm
from .models import EmailChange
from django.utils import timezone

import uuid



class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Requerido. carácteres como máximo y debe ser un email válido.",
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ingresado ya esta en uso.")
        return email

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]


class EmailChangeForm(forms.ModelForm):

    def clean_email(self):
        new_email = self.cleaned_data.get('new_email')
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("El email ingresado ya esta en uso.")
        return new_email

    class Meta:
        model= EmailChange
        fields = ['new_email']
        labels = {
            "new_email": "Nuevo email",
        }        


class VerifyTokenForm(forms.Form):
    token_part1 = forms.CharField(
        label='TOKEN 1',
        max_length=25,
        help_text='Token perteneciente al email antiguo del usuario.\n\nSe distinguen mayusucas de minisculas',
    )

    token_part2 = forms.CharField(
        label='TOKEN 2',
        max_length=25,
        help_text='Token perteneciente al email nuevo del usuario.\n\nSe distinguen mayusucas de minisculas',
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()

        try:
            email_change = self.get_email_change_object()
        except EmailChange.DoesNotExist:
            raise forms.ValidationError('No se encontró una solicitud de cambio de correo electrónico para este usuario.')
        
        if not email_change:
            raise forms.ValidationError('El token de verificación no es válido.')

        if email_change.expiration_time < timezone.now():
            raise forms.ValidationError('El token de verificación ha expirado.')

        return cleaned_data


    def get_email_change_object(self):
        token_part1 = self.cleaned_data.get('token_part1')
        token_part2 = self.cleaned_data.get('token_part2')

        token = f'{token_part1}-{token_part2}'  # Concatenar las partes del token

        try:
            # Validar y convertir el token a UUID
            token_uuid = uuid.UUID(token)

            # Realizar la consulta utilizando el token UUID
            email_change = EmailChange.objects.get(user=self.user, token=token_uuid)

            return email_change
        
        except (ValueError, TypeError, EmailChange.DoesNotExist):
            raise forms.ValidationError('No se encontró una solicitud de cambio de correo electrónico para este usuario.')
