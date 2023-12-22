# Generated by Django 5.0 on 2023-12-22 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='location',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]