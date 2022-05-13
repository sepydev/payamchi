from django.contrib import admin
from .models import Contact
from .models import MessageTemplate

admin.site.register(Contact)
admin.site.register(MessageTemplate)

