# Generated by Django 5.0 on 2024-08-22 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codedictionapp', '0015_alter_contactus_uploaded_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subjects',
            options={},
        ),
        migrations.RemoveField(
            model_name='subjects',
            name='position',
        ),
        migrations.CreateModel(
            name='CourseSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.courses')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.subjects')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('course', 'subject')},
            },
        ),
    ]
