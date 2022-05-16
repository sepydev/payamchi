from django.db import models
from django.utils.translation import gettext_lazy as _


class OTP(models.Model):
    create_date = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)
    secret_code = models.CharField(verbose_name=_('کد تائید'), max_length=20)
    mobile = models.CharField(
        _('موبایل'),
        max_length=11,
    )
