# Generated by Django 5.0 on 2024-02-09 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_remove_post_banner_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='alt',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
