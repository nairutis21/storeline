# Generated by Django 2.2.13 on 2021-09-10 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensor',
            old_name='sensor_type',
            new_name='pressure',
        ),
        migrations.AddField(
            model_name='sensor',
            name='temp',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
