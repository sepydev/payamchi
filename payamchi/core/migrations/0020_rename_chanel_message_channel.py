# Generated by Django 4.0.4 on 2022-07-15 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_rename_chanel_channel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='chanel',
            new_name='channel',
        ),
    ]
