from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_model import BaseModel
from .contact import Contact
from .message import Message

User = get_user_model()


class MessageReceiverStatusChoices(models.IntegerChoices):
    UNDEFINED = 1, 'نامشخص'
    SUCCESSFUL = 2, 'موفق'
    UNSUCCESSFUL = 3, 'ناموفق'


class MessageReceiver(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('نام کاربری')
    )
    message = models.ForeignKey(
        Message,
        verbose_name=_('پیام'),
        on_delete=models.CASCADE,
    )
    contact = models.ForeignKey(
        Contact,
        verbose_name=_('مخاطب'),
        on_delete=models.CASCADE,
    )
    status = models.SmallIntegerField(
        verbose_name=_('وضعیت'),
        choices=MessageReceiverStatusChoices.choices,
        default=MessageReceiverStatusChoices.UNDEFINED.value,
    )
    send_date = models.DateTimeField(
        verbose_name=_('تاریخ ارسال'),
        null=True,
        blank=True,
    )
    deliver_date = models.DateTimeField(
        verbose_name=_('تاریخ تحویل'),
        null=True,
        blank=True,
    )
    error_number = models.IntegerField(
        verbose_name=_('کد خطای ناموفق'),
        null=True,
        blank=True,
    )
    effort_count = models.SmallIntegerField(
        verbose_name=_('تعداد تلاش انجام شده'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'دریافت کننده پیام'
        verbose_name_plural = 'دریافت کننده های پیام'

    def __str__(self):
        return self.contact.caption + ' ' + self.message.caption
