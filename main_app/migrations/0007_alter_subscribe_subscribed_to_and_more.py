# Generated by Django 4.2.4 on 2023-11-14 07:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0006_rename_subscription_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribe',
            name='subscribed_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_subscribers',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_subscriptions',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
