# Generated by Django 3.2.5 on 2022-04-15 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0005_auto_20220413_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='date_ended',
            field=models.DateTimeField(blank=True, null=True, verbose_name='结束日期'),
        ),
        migrations.AlterField(
            model_name='service',
            name='date_started',
            field=models.DateTimeField(blank=True, null=True, verbose_name='开始日期'),
        ),
    ]
