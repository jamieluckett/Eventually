# Generated by Django 2.0.1 on 2018-02-11 23:30

from django.db import migrations, models
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_auto_20180211_1802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventline',
            options={},
        ),
        migrations.AddField(
            model_name='eventline',
            name='invite_key',
            field=models.CharField(default=event.models.generate_key, max_length=6),
        ),
    ]
