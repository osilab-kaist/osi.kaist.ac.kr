# Generated by Django 2.2.27 on 2022-03-21 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220321_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='year',
        ),
    ]
