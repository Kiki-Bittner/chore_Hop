# Generated by Django 3.1.7 on 2021-04-06 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chore_app', '0005_auto_20210405_2021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='phone_number',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
