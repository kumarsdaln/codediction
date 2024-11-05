from django import forms
from codedictionapp.models import *
import readtime
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from studentdashboard.models import StudentProfile,Education

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', 'brief', 'description', 'icon', 'image', 'slug', 'meta_data']
class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory 
        fields = ['name','slug','meta_data']
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['category','title','slug','brief','description','image','meta_data']

    def save(self, commit=True,user=None,uploaded_at=False):
        instance = super().save(commit=False)  # Don't save to database yet
        # Perform additional actions with the form data
        read_time=readtime.of_html(self.cleaned_data['description'])
        
        instance.read_time=read_time
        # form.cleaned_data['category']=category
        if user:
            instance.uploaded_by = user
        if uploaded_at:    
            instance.uploaded_at=datetime.datetime.now()
        instance.updated_at=datetime.datetime.now()
        if commit:
            instance.save()  # Save to database if commit is True
        return instance
class SubjectTypeForm(forms.ModelForm):
    class Meta:
        model = SubjectType
        fields = ['name','slug','meta_data']
class SubjectsForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ['name','icon','price','time_period','description','slug','subject_type','relation_with','meta_data']
class CourseCategoriesForm(forms.ModelForm):
    class Meta:
        model = CourseCategories
        fields = ['name','slug','meta_data']
class CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['name','image','description','slug','subjects','course_category','meta_data', 'price']       
class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['subject','title','slug','description','relation_with','meta_data']  
class OurBatchForm(forms.ModelForm):
    class Meta:
        model = OurBatch
        fields = ['course','batch_name','slug','description','image','start_at','batch_time','language','meta_data']  
class WorkCategoriesForm(forms.ModelForm):
    class Meta:
        model = WorkCategories
        fields = ['name', 'slug', 'meta_data']
class OurWorkForm(forms.ModelForm):
    class Meta:
        model = OurWork
        fields = ['name', 'image', 'description', 'slug', 'work_category', 'meta_data']
class OurClientsForm(forms.ModelForm):  
    class Meta:
        model = OurClients
        fields = ['name', 'image']
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'designation', 'photo', 'testimonial'] 

class ContactusForm(forms.ModelForm):
    class Meta:
        model = Contactus
        fields = ['name', 'email', 'phone', 'subject', 'message', 'uploaded_at']
class SubscribeNewsletter(forms.ModelForm):
    class Meta:
        model = SubscribeNewsletter
        fields = ['email', 'uploaded_at']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=[('S', 'Student'), ('T', 'Teacher')], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SocialMediaPlatformForm(forms.ModelForm):
    class Meta:
        model = SocialMediaPlatform
        fields = ['name', 'icon']

class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=55)

    class Meta:
        model = StudentProfile
        fields = [
            'first_name', 'last_name', 'designation', 'phone', 'bio', 
            'photo', 'dob', 'location', 'email', 'username'
        ]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['username'].initial = user.username

    def save(self, commit=True):
        profile = super(StudentProfileForm, self).save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.last_name = self.cleaned_data['email']
        user.last_name = self.cleaned_data['username']
        if commit:
            user.save()
            profile.save()
        return profile  
    
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'start_year', 'end_year', 'description']

    def __init__(self, *args, **kwargs):
        self.student_profile = kwargs.pop('student_profile', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.student_profile:
            instance.student = self.student_profile
        if commit:
            instance.save()
        return instance
    