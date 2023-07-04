from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView
)
from .views import SignUpView, send_mail_change, verify_change_email
from core.views import HomePageView

urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(template_name = 'login/signup.html'), name='signup'),
    path('accounts/login/', LoginView.as_view(template_name='login/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='login/logout'), name='logout'),
    path('accounts/password-reset/', PasswordResetView.as_view(template_name='resets/password/password_reset_form.html'),name='password-reset'),
    path('accounts/password-reset/done/', PasswordResetDoneView.as_view(template_name='resets/password/password_reset_done.html'),name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='resets/password/password_reset_confirm.html'),name='password_reset_confirm'),
    path('', HomePageView.as_view(), name='password_reset_complete'),
    path('accounts/change-email/', send_mail_change, name='email-change'),
    path('accounts/change-email/verify', verify_change_email, name='verify-token'),
]