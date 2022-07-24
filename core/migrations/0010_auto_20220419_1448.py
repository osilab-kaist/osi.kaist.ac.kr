# Generated by Django 2.2.5 on 2022-04-19 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20220419_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='code_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='pdf_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='video_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]