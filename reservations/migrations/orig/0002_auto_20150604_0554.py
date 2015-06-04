# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date_reserved',
            field=models.DateTimeField(null=True, default='2015-01-01'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='title',
            field=models.CharField(max_length=55, null=True, blank=True),
        ),
    ]
