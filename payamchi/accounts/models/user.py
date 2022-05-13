from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(UserManager):
    pass


class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'مدیر سیستم'
    OPERATOR = 'operator', 'اوپراتور'
    CLIENT = 'client', 'کاربر'


class User(AbstractUser):
    username = models.CharField(
        _('نام کاربری'),
        max_length=150,
        unique=True,
        help_text=_('حداکثر ۱۵۰ کاراکتر شامل حروف و اعداد'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("یک کاربر با این نام کاربری وجود دارد"),
        },
    )
    password = models.CharField(_('کلمه عبور'), max_length=128)
    last_login = models.DateTimeField(_('آخرین ورود'), blank=True, null=True)
    first_name = models.CharField(_('نام'), max_length=150, blank=True)
    last_name = models.CharField(_('نام خانوادگی'), max_length=150, blank=True)
    email = models.EmailField(_('پست الکترونیک'), blank=True)
    is_active = models.BooleanField(
        _('فعال'),
        default=True,
        help_text=_(
            'مشخص می کند که آیا این کاربر فعال است. '
            'بجای حذف کاربر تیک این مورد را بردارید'
        ),
    )
    mobile = models.CharField(_('موبایل'), max_length=11, blank=True)
    ir_code = models.CharField(_('کد ملی'), max_length=10, blank=True)
    father = models.CharField(_('نام پدر'), max_length=150, blank=True)
    register_date = models.DateTimeField(_('تاریخ ثبت نام'), auto_now=True)
    role = models.CharField(
        _('نقش'),
        choices=RoleChoices.choices,
        max_length=10,
        blank=False,
        null=False,
        default=RoleChoices.CLIENT.value
    )
    voice_mobile_cost = models.BigIntegerField(_('هزینه پیام صوتی موبایل'), null=False, default=700)
    voice_tel_cost = models.BigIntegerField(_('هزینه پیام صوتی تلفن'), null=False, default=700)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
