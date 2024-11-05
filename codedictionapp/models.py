from django.db import models
from django.contrib.auth.models import User
import datetime

#Services
class Services(models.Model):
    name = models.CharField(max_length=50)
    brief = models.CharField(max_length=1000)
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
    status = models.BooleanField(default=True)
    price = models.FloatField(default=0)
    def __str__(self):
        return f"{self.name}"

class CourseSubject(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='course_subject')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ['course', 'subject']
        ordering = ['order']

    def __str__(self):
        return f"{self.course.name} - {self.subject.name} ({self.order})"


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
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['order']

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
    
class SocialMediaPlatform(models.Model):
    name = models.CharField(max_length=100)
    icon = models.TextField()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username}'    