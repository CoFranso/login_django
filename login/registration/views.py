from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone

from .models import EmailChange
from .forms import UserCreationFormWithEmail, EmailChangeForm, VerifyTokenForm
from .utils import *


# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_c1ass=None):
        form = super(SignUpView, self).get_form()
        return form



# #---------------------------- EMAIL CHANGE ------------------------------------

@login_required
def send_mail_change(request):
    form = EmailChangeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            
            # Generar token y guardar en la base de datos
            expiration_time = timezone.now() + timezone.timedelta(hours=24)
            email_change = EmailChange.objects.create(
                user=request.user,
                new_email=new_email,
                expiration_time=expiration_time
                )

            token = email_change.token
            
            # Convertir el token a cadena
            token_str = str(token)

            # Dividir el token en dos partes
            half_length = len(token_str) // 2
            token_part1 = token_str[:half_length]
            token_part2 = token_str[half_length:]

            # Enviar correo electrónico al correo actual
            current_email_subject = 'Cambio de correo electrónico solicitado'
            current_email_message = f'Hola {request.user.username}, has solicitado cambiar tu dirección de correo electrónico actual a {new_email}.\n\nPara completar el cambio, ingresa el siguiente token (parte 1 de 2) de verificación en el formulario: {token_part1}\n\nSi no has solicitado este cambio, ignora este correo electrónico.\n\nGracias.'
            send_mail(current_email_subject, current_email_message, 'smtp.'+get_email_provider(request.user.email), [request.user.email])
            
            # Enviar correo electrónico al nuevo correo electrónico
            new_email_subject = 'Cambio de correo electrónico solicitado'
            new_email_message = f'Hola,\n\nSe ha solicitado un cambio de email del usuario {request.user.username} a {new_email} en nuestro sitio web.\n\nPara completar el cambio, ingresa el siguiente token (parte 2 de 2) de verificación en el formulario: {token_part2}\n\nSi no has solicitado este cambio, ignora este correo electrónico.\n\nGracias.'
            send_mail(new_email_subject, new_email_message, 'smtp.'+get_email_provider(new_email), [new_email])
            
            # Mostrar mensaje de éxito
            messages.success(request, 'Se ha enviado una parte del token a cada email del usuario.')
            return redirect('verify-token')  # Reemplaza 'nombre_de_la_vista' por el nombre de la vista a la que deseas redirigir
    
    return render(request, 'resets/email/change_email_form.html', {'form': form})



@login_required
def verify_change_email(request):
    form = VerifyTokenForm(request.user, request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            email_change = form.get_email_change_object()
            # Realizar el cambio de correo electrónico
            user = email_change.user
            new_email = email_change.new_email

            # Actualizar el correo electrónico del usuario
            user.email = new_email
            user.save()

            # Eliminar el objeto EmailChange
            email_change.delete()

            # Mostrar un mensaje de éxito
            messages.success(request, '¡El cambio de correo electrónico se ha realizado con éxito!')
            return redirect('home')

    return render(request, 'resets/email/change_email_verify.html', {'form': form})