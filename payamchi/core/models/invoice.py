from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base_model import BaseModel

User = get_user_model()


class Invoice(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('نام کاربری'))
    invoice_number = models.BigIntegerField(
        verbose_name=_('شماره فاکتور'),
    )
    pay_date = models.DateTimeField(
        verbose_name=_('تاریخ پرداخت'),
        null=True,
        blank=True,
    )
    amount = models.BigIntegerField(
        verbose_name=_('مبلغ'),
    )
    pay_code = models.BigIntegerField(
        verbose_name=_('کد پیگیری'),
    )

    @property
    def tax(self):
        return round(self.amount * 9 / 100)

    tax.fget.short_description = 'مالیات'

    @property
    def total_amount(self):
        return self.amount + self.tax

    total_amount.fget.short_description = 'قابل پرداخت'

    class Meta:
        verbose_name = 'فاکتور فروش'
        verbose_name_plural = 'فاکتور های فروش'
