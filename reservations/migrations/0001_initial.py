# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reserved', models.DateTimeField(default='2015-01-01', null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, null=True, max_length=55)),
                ('description', models.TextField(blank=True, null=True, max_length=450)),
                ('confirmed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Reservations',
            },
        ),
    ]
