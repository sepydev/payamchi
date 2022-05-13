from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_model import StatusChoices
from .campaign import Campaign
from .message_template import MessageTemplate, MessageTypeChoices

User = get_user_model()


class Message(models.Model):
    caption = models.CharField(verbose_name=_('عنوان'), max_length=250)
    create_date = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)
    modify_date = models.DateTimeField(verbose_name='تاریخ آخرین ویرایش', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نام کاربری'))
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name=_('کمپین'))
    send_date = models.DateTimeField(verbose_name=_('تاریخ ارسال'))
    status = models.IntegerField(
        verbose_name=_('وضعیت'),
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT.value
    )
    cost = models.BigIntegerField(verbose_name=_('هزینه پیام'))
    message_type = models.CharField(
        verbose_name=_('نوع پیام'),
        choices=MessageTypeChoices.choices,
        max_length=10,
        default=MessageTypeChoices.VOICE.value
    )
    message_template = models.ForeignKey(
        MessageTemplate,
        on_delete=models.CASCADE,
        verbose_name=_('قالب پیام'),
        null=True,
        blank=True,
    )
    effort = models.PositiveSmallIntegerField(
        verbose_name=_('تعداد تلاش'),
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    send_effort_delay = models.PositiveIntegerField(
        verbose_name=_('تاخیر ارسال پیام'),
        default=600
    )

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
