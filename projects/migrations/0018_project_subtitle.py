# Generated by Django 5.0.2 on 2024-03-13 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_alter_project_options_remove_project_publish_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='subtitle',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
