# Generated by Django 5.1 on 2024-08-28 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codedictionapp', '0016_alter_subjects_options_remove_subjects_position_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curriculum',
            options={},
        ),
        migrations.RemoveField(
            model_name='curriculum',
            name='position',
        ),
    ]
