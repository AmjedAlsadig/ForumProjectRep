# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-04-10 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForumAccount', '0010_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='read_at',
            field=models.DateTimeField(null=True),
        ),
    ]
