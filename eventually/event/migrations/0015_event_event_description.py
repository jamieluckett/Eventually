# Generated by Django 2.0.1 on 2018-02-12 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0014_event_event_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_description',
            field=models.CharField(default='', max_length=250),
        ),
    ]
