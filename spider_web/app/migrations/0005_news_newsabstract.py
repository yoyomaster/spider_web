# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151014_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='newsAbstract',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
