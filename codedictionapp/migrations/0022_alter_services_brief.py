# Generated by Django 5.1 on 2024-08-31 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codedictionapp', '0021_ourteam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='brief',
            field=models.CharField(max_length=1000),
        ),
    ]
