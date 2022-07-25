from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .contact_define_label import ContactDefineLabel
from .channel import Channel
from .base_model import BaseModel
from .campaign import Campaign
from .message_define_label import MessageDefineLabel
from .message_template import MessageTemplate, MessageTypeChoices

User = get_user_model()


class MessageStatusChoices(models.IntegerChoices):
    DRAFT = 1, 'پیشنویس'
    READY_TO_SEND = 2, 'آماده ارسال'
    CONFIRM = 3, 'تایید'
    SEND = 4, 'ارسال'
    DELIVER = 5, 'دلیور شده'
    CANCEL = 6, 'لغو شده'


class Message(BaseModel):
    caption = models.CharField(verbose_name=_('عنوان'), max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نام کاربری'))
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name=_('کانال ارسال'), null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, verbose_name=_('کمپین'), null=True, blank=True)
    send_date = models.DateTimeField(verbose_name=_('تاریخ ارسال'))
    status = models.IntegerField(
        verbose_name=_('وضعیت'),
        choices=MessageStatusChoices.choices,
        default=MessageStatusChoices.DRAFT.value
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
    labels = models.ManyToManyField(
        MessageDefineLabel,
        verbose_name=_('برچسب ها'),
        blank=True,
    )
    contact_labels = models.ManyToManyField(
        ContactDefineLabel,
        verbose_name=_('برچسب های مخاطب'),
        blank=True,
    )

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return self.caption
