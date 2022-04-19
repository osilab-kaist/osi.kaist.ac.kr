# Generated by Django 2.2.5 on 2022-04-19 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_project_previous_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='previous_members',
            field=models.TextField(blank=True, help_text="E.g., 'Yoshua Bengio, Yann LeCun and Geoffrey Hinton'", null=True),
        ),
    ]