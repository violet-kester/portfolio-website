# Generated by Django 5.0 on 2024-01-11 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_screenshot_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='logo',
            field=models.ImageField(default='static/img/logos/logo-480.png', upload_to='projects/static/projects/img/logos/'),
        ),
    ]
