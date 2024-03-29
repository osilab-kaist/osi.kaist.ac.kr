# Generated by Django 2.2.5 on 2023-02-04 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_admintoken_gpustatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='scholar',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
    ]
