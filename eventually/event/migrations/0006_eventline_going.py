# Generated by Django 2.0.1 on 2018-02-08 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20180126_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventline',
            name='going',
            field=models.BooleanField(default=False),
        ),
    ]
