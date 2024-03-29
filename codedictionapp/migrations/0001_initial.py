# Generated by Django 5.0 on 2024-01-30 15:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_tags', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_data', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/images')),
                ('alt', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OurClients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='uploads/clients')),
            ],
        ),
        migrations.CreateModel(
            name='OurStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('photo', models.ImageField(upload_to='uploads/student')),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('brief', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_data', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('meta_data', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('photo', models.ImageField(upload_to='uploads/testimonial')),
                ('testimonial', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('meta_data', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('desciption', models.TextField()),
                ('image', models.ImageField(upload_to='uploads/blog/')),
                ('read_time', models.CharField(max_length=10)),
                ('meta_tags', models.TextField()),
                ('status', models.BooleanField(default=1)),
                ('uploaded_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('uploaded_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.blogcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='uploads/courses/')),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('meta_data', models.TextField(null=True)),
                ('course_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.coursecategories')),
            ],
        ),
        migrations.CreateModel(
            name='OurBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='uploads/batch')),
                ('start_at', models.DateField()),
                ('batch_time', models.CharField(max_length=55)),
                ('language', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('u', 'Upcoming'), ('r', 'Runnig'), ('c', 'Completed')], default='u', max_length=2)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.courses')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('meta_data', models.TextField(null=True)),
                ('question_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('meta_data', models.TextField(null=True)),
                ('answer_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.question')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ImageField(upload_to='uploads/subjects/')),
                ('price', models.FloatField()),
                ('time_period', models.IntegerField()),
                ('description', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('meta_data', models.TextField(null=True)),
                ('relation_with', models.ManyToManyField(to='codedictionapp.subjects')),
                ('subject_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.subjecttype')),
            ],
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('meta_data', models.TextField(null=True)),
                ('relation_with', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.curriculum')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.subjects')),
            ],
        ),
        migrations.AddField(
            model_name='courses',
            name='subjects',
            field=models.ManyToManyField(to='codedictionapp.subjects'),
        ),
        migrations.CreateModel(
            name='OurWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='uploads/ourwork/')),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('meta_data', models.TextField(null=True)),
                ('work_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='codedictionapp.workcategories')),
            ],
        ),
    ]
