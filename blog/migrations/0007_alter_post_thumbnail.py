# Generated by Django 5.0 on 2024-01-11 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comment_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='static/img/logos/logo-480.png', upload_to='blog/static/blog/img/thumbnails/'),
        ),
    ]