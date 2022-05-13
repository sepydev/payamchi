from django.contrib import admin
from .models import Contact, MessageTemplate, Campaign

admin.site.register(Contact)
admin.site.register(MessageTemplate)
admin.site.register(Campaign)
