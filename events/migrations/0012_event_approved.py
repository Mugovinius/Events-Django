# Generated by Django 4.1.5 on 2023-02-08 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_alter_venue_venue_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
    ]
