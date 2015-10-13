# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=512)),
                ('content_time', models.DateTimeField()),
                ('comment_parent_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newsType', models.CharField(max_length=20)),
                ('newsLable', models.CharField(max_length=20, blank=True)),
                ('newsTitle', models.CharField(max_length=128)),
                ('newsContent', models.TextField(max_length=51200)),
                ('picture_id', models.IntegerField(null=True, blank=True)),
                ('browseNumber', models.IntegerField(default=0)),
                ('commentNumber', models.IntegerField(default=0)),
                ('likesNumber', models.IntegerField(default=0)),
                ('newsTime', models.DateTimeField(auto_now=True)),
                ('newsUrl', models.URLField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.URLField(max_length=256)),
                ('pictureID', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userGrade', models.IntegerField(default=1)),
                ('userImage', models.ImageField(default=b'static/image/default.gif', null=True, upload_to=b'static/user_image', blank=True)),
                ('loginCount', models.IntegerField(default=1)),
                ('lastLogin', models.DateTimeField(auto_now=True)),
                ('likeCount', models.IntegerField(default=0)),
                ('commentCount', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comments',
            name='news_id',
            field=models.ForeignKey(to='app.News'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
