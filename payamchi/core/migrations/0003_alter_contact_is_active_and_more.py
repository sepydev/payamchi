# Generated by Django 4.0.4 on 2022-05-13 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_contact_create_date_contact_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='messagetemplate',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='وضعیت'),
        ),
    ]
