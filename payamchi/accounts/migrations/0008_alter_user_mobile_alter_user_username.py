# Generated by Django 4.0.4 on 2022-05-16 16:47

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_birth_date_alter_user_father_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(error_messages={'unique': 'یک کاربر با این نام کاربری وجود دارد'}, max_length=11, unique=True, verbose_name='موبایل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='حداکثر ۱۵۰ کاراکتر شامل حروف و اعداد', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='نام کاربری'),
        ),
    ]