# Generated by Django 5.0 on 2023-12-13 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='thumbnail',
            field=models.ImageField(default='static/img/thumbnails/default_thumbnail.png', upload_to='portfolio/static/img/thumbnails/'),
        ),
    ]
