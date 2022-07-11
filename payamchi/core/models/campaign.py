import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_model import BaseModel

User = get_user_model()


class Campaign(BaseModel):
    caption = models.CharField(verbose_name=_('عنوان'), max_length=250)
    start_date = models.DateTimeField(verbose_name=_('تاریخ شروع'))
    end_date = models.DateTimeField(verbose_name=_('تاریخ پایان'))
    description = models.TextField(verbose_name=_('توضیحات'), null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نام کاربری'))

    def is_expire(self):
        return self.end_date.timestamp() < datetime.datetime.now().timestamp()

    class Meta:
        verbose_name = 'کمپین'
        verbose_name_plural = 'کمپین ها'

    def __str__(self):
        return self.caption

    def __repr__(self):
        return self.caption
