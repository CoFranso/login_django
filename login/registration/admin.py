from django.contrib import admin
from .models import EmailChange

class EmailChangeAdmin(admin.ModelAdmin):
    list_display = ['user', 'new_email', 'expiration_time']
    search_fields = ['user__username', 'new_email']
    readonly_fields = ['user', 'new_email', 'expiration_time']

admin.site.register(EmailChange, EmailChangeAdmin)
