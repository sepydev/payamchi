from django.db import models
from django.utils.translation import gettext_lazy as _





class BaseModel(models.Model):
    is_active = models.BooleanField(verbose_name=_('فعال'), default=True)
    create_date = models.DateTimeField(verbose_name=_('تاریخ ایجاد'), auto_now_add=True)
    modify_date = models.DateTimeField(verbose_name='تاریخ آخرین ویرایش', auto_now=True)

    class Meta:
        abstract = True
