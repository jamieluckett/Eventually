# Generated by Django 2.0.1 on 2018-02-12 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0015_event_event_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_description',
            field=models.CharField(default='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sollicitudin dolor nec placerat cursus. In facilisis dui vel tortor suscipit vestibulum. Etiam leo massa, auctor sed finibus sit amet, faucibus at nulla. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque quis sagittis purus. Mauris dictum pharetra leo, quis condimentum nisl mattis et. Nunc dignissim urna sit amet porta viverra. Nullam rutrum ligula libero, nec auctor augue ullamcorper in. Vivamus accumsan ipsum id blandit condimentum. Vestibulum lobortis accumsan mi, in facilisis nunc rhoncus sit amet. Curabitur ac magna id odio aliquam vestibulum. Sed vel scelerisque ex. Cras egestas ex dui.', max_length=500),
        ),
    ]
