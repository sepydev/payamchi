# Generated by Django 4.0.4 on 2022-07-10 13:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0018_alter_campaign_description'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Chanel',
            new_name='Channel',
        ),
    ]
