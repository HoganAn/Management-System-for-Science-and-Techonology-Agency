# Generated by Django 3.2.5 on 2022-04-13 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0003_remove_service_director'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='state',
            field=models.BooleanField(default=False, verbose_name='完成状态'),
        ),
        migrations.AddField(
            model_name='service',
            name='state',
            field=models.BooleanField(default=False, verbose_name='完成状态'),
        ),
    ]
