# Generated by Django 3.1.7 on 2021-04-07 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chore_app', '0009_auto_20210407_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chore',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
