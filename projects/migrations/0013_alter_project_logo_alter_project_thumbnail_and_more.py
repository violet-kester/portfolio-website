# Generated by Django 5.0.2 on 2024-03-05 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_screenshot_description_alter_link_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='logo',
            field=models.ImageField(default='img/logos/portfolio-logo-480.png', upload_to='projects/img/logos/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='thumbnail',
            field=models.ImageField(default='img/logos/portfolio-logo-480.png', upload_to='projects/img/thumbnails/'),
        ),
        migrations.AlterField(
            model_name='screenshot',
            name='image',
            field=models.ImageField(upload_to='projects/img/screenshots/'),
        ),
    ]
