# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-16 00:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignatures', '0004_auto_20180727_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='ufavisos',
            name='uf',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='assignatures.UF'),
            preserve_default=False,
        ),
    ]
