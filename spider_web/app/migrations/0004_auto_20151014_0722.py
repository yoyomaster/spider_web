# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_comments_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='username',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
    ]
