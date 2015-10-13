# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='userImage',
            field=models.ImageField(null=True, upload_to=b'user_image', blank=True),
            preserve_default=True,
        ),
    ]
