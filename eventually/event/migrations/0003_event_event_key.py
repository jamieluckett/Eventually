# Generated by Django 2.0.1 on 2018-01-25 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20180125_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_key',
            field=models.CharField(default=1, max_length=6),
            preserve_default=False,
        ),
    ]