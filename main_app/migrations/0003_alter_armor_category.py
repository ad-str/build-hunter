# Generated by Django 5.0 on 2023-12-17 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_skill_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='armor',
            name='category',
            field=models.CharField(choices=[('head', 'Head'), ('chest', 'Chest'), ('arm', 'Arm'), ('waist', 'Waist'), ('leg', 'Leg')], max_length=5),
        ),
    ]
