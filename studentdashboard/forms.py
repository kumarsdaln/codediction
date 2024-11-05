from django import forms
from studentdashboard.models import *
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = StudentProfile
        fields = [
            'first_name', 'last_name', 'designation', 'phone', 'bio', 
            'photo', 'dob', 'location'
        ]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        profile = super(StudentProfileForm, self).save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
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
    
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']

    def save(self, commit=True, student=None):
        instance = super().save(commit=False)
        if student:
            instance.student = student
        if commit:
            instance.save()
        return instance    
    
class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ['platform', 'link']