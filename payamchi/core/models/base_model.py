from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.IntegerChoices):
    DRAFT = 1, 'پیشنویس'
    READY_TO_SEND = 2, 'آماده ارسال'
    CONFIRM = 3, 'تایید'
    SEND = 4, 'ارسال'
    DELIVER = 5, 'دلیور شده'
    CANCEL = 6, 'لغو شده'


class BaseModel(models.Model):
    is_active = models.BooleanField(verbose_name=_('وضعیت'), default=False)
    create_date = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)
    modify_date = models.DateTimeField(verbose_name='تاریخ آخرین ویرایش', auto_now=True)

    class Meta:
        abstract = True
