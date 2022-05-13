from django.contrib import admin

from .models import (
    Contact,
    MessageTemplate,
    Campaign,
    Message,
    MessageReceiver,
    MessageDefineLabel,
)

admin.site.register(Contact)
admin.site.register(MessageTemplate)
admin.site.register(Campaign)
admin.site.register(Message)
admin.site.register(MessageReceiver)
admin.site.register(MessageDefineLabel)
