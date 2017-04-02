# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_auto_20170206_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostViewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.ForeignKey(to='blog.Post')),
                ('viewer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
