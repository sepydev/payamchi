from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_model import BaseModel
from .message_template import MessageTypeChoices

User = get_user_model()


class Channel(BaseModel):
    caption = models.CharField(verbose_name=_('عنوان'), max_length=250)
    message_type = models.CharField(
        verbose_name=_('نوع پیام'),
        choices=MessageTypeChoices.choices,
        max_length=10,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نام کاربری'), null=True, blank=True)

    token = models.CharField(verbose_name=_('شناسه کانال'), max_length=250, blank=True, null=True)
    user_name = models.CharField(verbose_name=_('نام کاربری'), max_length=150, blank=True, null=True)
    password = models.CharField(verbose_name=_('رمز عبور'), max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'کانال'
        verbose_name_plural = 'کانال ها'

    def __repr__(self):
        return self.caption

    def __str__(self):
        return self.caption
