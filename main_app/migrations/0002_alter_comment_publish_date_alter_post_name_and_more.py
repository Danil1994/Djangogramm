# Generated by Django 4.2.4 on 2023-11-10 09:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='publish_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='pubdate'),
        ),
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='pubdate'),
        ),
    ]