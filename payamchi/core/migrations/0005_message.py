# Generated by Django 4.0.4 on 2022-05-13 11:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_campaign'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=250, verbose_name='عنوان')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین ویرایش')),
                ('send_date', models.DateTimeField(verbose_name='تاریخ ارسال')),
                ('status', models.IntegerField(choices=[(1, 'پیشنویس'), (2, 'آماده ارسال'), (3, 'تایید'), (4, 'ارسال'), (5, 'دلیور شده'), (6, 'لغو شده')], default=1, verbose_name='وضعیت')),
                ('cost', models.BigIntegerField(verbose_name='هزینه پیام')),
                ('message_type', models.CharField(choices=[('voice', 'صوتی'), ('sms', 'پیامک'), ('email', 'ایمیل'), ('telegram', 'تلگرام'), ('whatsapp', 'واتس اپ')], default='voice', max_length=10, verbose_name='نوع پیام')),
                ('effort', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='تعداد تلاش')),
                ('send_effort_delay', models.PositiveIntegerField(default=600, verbose_name='تاخیر ارسال پیام')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.campaign', verbose_name='کمپین')),
                ('message_template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.messagetemplate', verbose_name='قالب پیام')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نام کاربری')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': 'پیام ها',
            },
        ),
    ]
