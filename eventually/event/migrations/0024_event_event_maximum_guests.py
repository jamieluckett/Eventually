# Generated by Django 2.0.1 on 2018-04-14 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0023_auto_20180414_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_maximum_guests',
            field=models.IntegerField(default=0, help_text='Maximum number of guests'),
        ),
    ]
