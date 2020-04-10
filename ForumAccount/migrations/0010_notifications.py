# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-04-10 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ForumAccount', '0009_auto_20200409_2259'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ForumAccount.Post')),
                ('receivers', models.ManyToManyField(related_name='receiver', to='ForumAccount.UserProfile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='ForumAccount.UserProfile')),
            ],
        ),
    ]