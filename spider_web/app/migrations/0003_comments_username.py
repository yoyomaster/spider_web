# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20151014_0409'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='username',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
    ]
