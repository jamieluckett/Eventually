# Generated by Django 2.0.1 on 2018-04-11 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guestgroup',
            name='event_creator',
        ),
        migrations.RemoveField(
            model_name='guestgroup',
            name='event_date_created',
        ),
    ]