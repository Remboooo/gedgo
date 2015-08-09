# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gedgo', '0002_auto_20150403_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
    ]
