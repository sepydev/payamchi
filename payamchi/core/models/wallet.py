from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_model import BaseModel
from .invoice import Invoice
from .message import Message

User = get_user_model()


class TransactionTypeChoices(models.IntegerChoices):
    INCREASE_CREDIT = 1, 'افزایش اعتبار'
    REFUND = 2, 'عودت وجه'
    DECREASE_CREDIT = 3, 'کاهش اعتبار'


class Wallet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نام کاربری'))
    transaction_type = models.IntegerField(
        verbose_name=_('نوع تراکنش'),
        choices=TransactionTypeChoices.choices,
    )
    amount = models.BigIntegerField(
        verbose_name=_('مبلغ'),
    )
    transaction_date = models.DateTimeField(verbose_name=_('تاریخ ارسال'))

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        verbose_name=_('فاکتور فروش'),
        null=True,
        blank=True,
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name=_('پیام'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف های پول'
