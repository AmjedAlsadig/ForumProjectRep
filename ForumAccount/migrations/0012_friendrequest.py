# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-04-11 08:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ForumAccount', '0011_notifications_read_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_receiver', to='ForumAccount.UserProfile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_sender', to='ForumAccount.UserProfile')),
            ],
        ),
    ]
