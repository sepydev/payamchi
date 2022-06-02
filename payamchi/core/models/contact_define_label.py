from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_model import BaseModel

User = get_user_model()


class ContactDefineLabel(BaseModel):
    caption = models.CharField(verbose_name=_('عنوان'), max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نام کاربری'))

    class Meta:
        verbose_name = 'برچسب مخاطب'
        verbose_name_plural = 'برچسب های مخاطبین'

    def __str__(self):
        return self.caption
