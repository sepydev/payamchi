from functools import partial

from django import forms
from django.core.validators import RegexValidator

MobileValidator = partial(
    RegexValidator,
    regex=r'^\0?\d{11}$',
    message=(
        "شماره موبایل وارد شده معتبر نمی باشد"
    )
)
