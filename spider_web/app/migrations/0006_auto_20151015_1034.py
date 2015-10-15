# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_news_newsabstract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='newsAbstract',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
