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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_reserved', models.DateTimeField(default=b'2015-01-01', null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=b'55', null=True, blank=True)),
                ('description', models.TextField(max_length=450, null=True, blank=True)),
                ('confirmed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Reservations',
            },
            bases=(models.Model,),
        ),
    ]
