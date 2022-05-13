# Generated by Django 4.0.4 on 2022-05-13 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='messagetemplate',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='فعال'),
        ),
    ]
