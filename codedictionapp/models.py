from django.db import models
from django.contrib.auth.models import User
import datetime

#Services
class Services(models.Model):
    name = models.CharField(max_length=50)
    brief = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to='uploads/services/icon')
    image = models.ImageField(upload_to='uploads/services', default='')
    slug = models.SlugField(unique=True,null=False,blank=False)
    meta_data = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.name}"

#For Courses
class SubjectType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,null=False,blank=False)
    meta_data = models.TextField(null=True)
    def __str__(self):
        return f"{self.name}"
    
class Subjects(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='uploads/subjects/')
    price = models.FloatField()
    time_period = models.IntegerField()
    description = models.TextField()
    slug = models.SlugField(unique=True,null=False,blank=False)
    subject_type = models.ForeignKey(SubjectType, on_delete=models.CASCADE)
    relation_with = models.ManyToManyField('self', null=True, blank=True)
    meta_data = models.TextField(null=True)
    position = models.PositiveIntegerField(default=1)
    def save(self, *args, **kwargs):
        # Check if position is not set
        if not self.position:
            # Get the maximum position from existing instances
            max_position = Subjects.objects.aggregate(models.Max('id'))['id__max'] or 0
            # Increment the position for the current instance
            self.position = max_position + 1
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['position']
    def __str__(self):
        return f"{self.name}"
    
class CourseCategories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,null=False,blank=False)
    meta_data = models.TextField(null=True)
    def __str__(self):
        return f"{self.name}"

class Courses(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='uploads/courses/')
    description = models.TextField()
    slug = models.SlugField(max_length=255,unique=True,null=False,blank=False)
    subjects = models.ManyToManyField(Subjects)
    course_category = models.ForeignKey(CourseCategories, on_delete=models.CASCADE, null=True)
    meta_data = models.TextField(null=True)
    def __str__(self):
        return f"{self.name}"

#Batches
class OurBatch(models.Model):
    status_choices = (
      ('u', "Upcoming"),
      ('r', "Runnig"),
      ('c', "Completed"),
    )
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True,null=False,blank=False)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/batch')
    start_at = models.DateField()
    batch_time = models.CharField(max_length=55)
    language = models.CharField(max_length=255)
    meta_data = models.TextField(null=True)
    status = models.CharField(max_length=2, choices=status_choices, default='u')
    def __str__(self):
        return f"{self.course.name} -> {self.batch_name}"
                
class Curriculum(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE) 
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255,unique=True,null=False,blank=False)
    description = models.TextField()
    relation_with = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    meta_data = models.TextField(null=True) 
    position = models.PositiveIntegerField(default=1)
    def save(self, *args, **kwargs):
        # Check if position is not set
        if not self.position:
            # Get the maximum position from existing instances
            max_position = Curriculum.objects.aggregate(models.Max('id'))['id__max'] or 0
            # Increment the position for the current instance
            self.position = max_position + 1
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['position']
    def __str__(self):
        return f"{self.title}"

#Question Answer    
class Question(models.Model):
    question = models.CharField(max_length=400)
    created_at = models.DateTimeField()
    slug = models.SlugField(max_length=255,unique=True,null=False,blank=False)
    question_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    meta_data = models.TextField(null=True)
    def __str__(self):
        return f"{self.question}"  

class Answer(models.Model):
    answer = models.TextField()
    created_at = models.DateTimeField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    meta_data = models.TextField(null=True)
    def __str__(self):
        return f"{self.question}"

class Images(models.Model):
    image = models.ImageField(upload_to='uploads/images')
    alt = models.CharField(max_length=255) 

#For Blog.
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,null=False,blank=False)
    meta_data = models.TextField()
    def __str__(self):
        return self.name

class Blog(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    title = models.TextField()
    slug = models.SlugField(max_length=255,unique=True,null=False,blank=False)
    brief = models.CharField(max_length=255, default='')
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/blog/')
    read_time = models.CharField(max_length=10)
    meta_data = models.TextField()
    status = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    uploaded_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    def __str__(self):
        return f"{self.category} -> {self.title}"

#Our Work    
class WorkCategories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True,null=False,blank=False)
    meta_data = models.TextField(null=True)
    def __str__(self):
        return f"{self.name}"    

class OurWork(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='uploads/ourwork/')
    description = models.TextField()
    slug = models.SlugField(max_length=255,unique=True,null=False,blank=False)
    work_category = models.ForeignKey(WorkCategories, on_delete=models.CASCADE, null=True)
    meta_data = models.TextField(null=True)   
    def __str__(self):
        return f"{self.work_category.name} -> {self.name}" 
    
class OurClients(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/clients') 
    def __str__(self):
        return f"{self.name}"

class OurStudents(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='uploads/student')
    slug = models.SlugField(max_length=255,unique=True,null=False,blank=False)
    batch = models.CharField(max_length=255, default='One To One Mentorship')
    def __str__(self):
        return f"{self.name}"
class OurTeam(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='uploads/student')
    slug = models.SlugField(max_length=255,unique=True,null=False,blank=False)
    description = models.TextField()
    def __str__(self):
        return f"{self.name}"    

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='uploads/testimonial')
    testimonial = models.TextField()
    def __str__(self):
        return f"{self.name}"
    
class EnrollStudent(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20) 
    batch = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return f"{self.name}" 

class Contactus(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)   
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=500)
    uploaded_at = models.DateTimeField()
    def __str__(self):
        return f"{self.name}" 

class SubscribeNewsletter(models.Model):
    email = models.EmailField(max_length=255)  
    uploaded_at = models.DateTimeField() 
    def __str__(self):
        return f"{self.email}"  