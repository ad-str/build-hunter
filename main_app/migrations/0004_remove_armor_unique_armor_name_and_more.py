# Generated by Django 5.0 on 2023-12-19 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_armor_category'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='armor',
            name='unique_armor_name',
        ),
        migrations.RemoveConstraint(
            model_name='decoration',
            name='unique_decoration_name',
        ),
        migrations.RemoveConstraint(
            model_name='skill',
            name='unique_skill_name',
        ),
        migrations.AddField(
            model_name='armor',
            name='armorset_id',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='decoration',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='skill',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]