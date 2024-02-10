# Generated by Django 4.2.4 on 2023-11-10 14:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0004_remove_like_created_at_remove_like_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subscribed_to',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers',
                                   to=settings.AUTH_USER_MODEL)),
                ('subscriber',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions',
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]