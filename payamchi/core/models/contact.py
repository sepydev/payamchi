from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Contact(models.Model):
    caption = models.CharField(verbose_name=_('عنوان'), max_length=250)
    mobile = models.CharField(verbose_name=_('موبایل'), max_length=11, blank=True, null=True)
    tel = models.CharField(verbose_name=_('تلفن'), max_length=13, blank=True, null=True)
    email = models.EmailField(verbose_name=_('پست الکترونیک'), blank=True, null=True)
    telegram_id = models.CharField(verbose_name=_('تلگرام'), max_length=20, blank=True, null=True)
    whatsapp_id = models.CharField(verbose_name=_('واتس اپ'), max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نام کاربری'))

    class Meta:
        verbose_name = 'مخاطب'
        verbose_name_plural = 'مخاطبین'
