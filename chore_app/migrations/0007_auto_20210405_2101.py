# Generated by Django 3.1.7 on 2021-04-06 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chore_app', '0006_auto_20210405_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user_lvl',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='user_lvl',
        ),
    ]
