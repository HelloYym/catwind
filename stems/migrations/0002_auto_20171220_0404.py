# Generated by Django 2.0 on 2017-12-20 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stems', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qualitynews',
            old_name='address',
            new_name='location',
        ),
    ]
