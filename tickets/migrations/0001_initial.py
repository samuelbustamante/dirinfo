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
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': [b'-created_on'],
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(default=0, choices=[(0, 'Abierto'), (1, 'En proceso'), (2, 'Atrazado'), (3, 'Resuelto'), (4, 'Cerrado')])),
                ('priority', models.PositiveSmallIntegerField(default=1, choices=[(0, 'Baja'), (1, 'Normal'), (2, 'Alta')])),
                ('assigned', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': [b'-created_on'],
                'permissions': ((b'can_assigned', 'Can assigned'), (b'can_change_status', 'Can change status'), (b'can_view_priority', 'Can view priority'), (b'can_change_priority', 'Can change priority')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='ticket',
            field=models.ForeignKey(to='tickets.Ticket'),
            preserve_default=True,
        ),
    ]
