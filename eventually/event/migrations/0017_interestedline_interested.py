# Generated by Django 2.0.1 on 2018-04-08 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0016_auto_20180212_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='interestedline',
            name='interested',
            field=models.BooleanField(default=False),
        ),
    ]