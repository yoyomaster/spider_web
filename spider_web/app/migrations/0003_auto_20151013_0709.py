# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20151013_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userImage',
            field=models.ImageField(default=b'/static/image/default.gif', null=True, upload_to=b'user_image', blank=True),
            preserve_default=True,
        ),
    ]
