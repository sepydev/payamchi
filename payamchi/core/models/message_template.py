from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_model import BaseModel

User = get_user_model()


class MessageTypeChoices(models.TextChoices):
    VOICE = 'voice', 'صوتی'
    SMS = 'sms', 'پیامک'
    EMAIL = 'email', 'ایمیل'
    TELEGRAM = 'telegram', 'تلگرام'
    WHATSAPP = 'whatsapp', 'واتس اپ'


class MessageTemplate(BaseModel):
    caption = models.CharField(verbose_name=_('عنوان'), max_length=250)
    message_type = models.CharField(
        verbose_name=_('نوع پیام'),
        choices=MessageTypeChoices.choices,
        max_length=10,
    )
    message_content = models.TextField(verbose_name=_('محتوای پیام'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نام کاربری'))

    class Meta:
        verbose_name = 'قالب پیام'
        verbose_name_plural = 'قالبهای پیام'
