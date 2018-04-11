# Generated by Django 2.0.1 on 2018-04-11 21:06

import accounts.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0020_auto_20180410_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventOwnerLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Event')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GuestGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(help_text='Enter Group Name', max_length=50)),
                ('event_date_created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('group_key', models.CharField(default=accounts.models.generate_key, max_length=6)),
                ('event_creator', models.CharField(default='John Smith', help_text='Enter Your Name', max_length=75)),
                ('event_creator_id', models.IntegerField(default=0, help_text='ID')),
            ],
        ),
        migrations.AddField(
            model_name='groupline',
            name='group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.GuestGroup'),
        ),
        migrations.AddField(
            model_name='groupline',
            name='guest_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Guest'),
        ),
    ]
