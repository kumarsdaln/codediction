# Generated by Django 5.1 on 2024-08-29 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codedictionapp', '0018_ourteam_meta_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]