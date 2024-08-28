from django import forms
from codedictionapp.models import *
import readtime
import datetime

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
        fields = ['name','image','description','slug','subjects','course_category','meta_data']   
class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['subject','title','slug','description','relation_with','meta_data']  
class OurBatchForm(forms.ModelForm):
    class Meta:
        model = OurBatch
        fields = ['course','batch_name','slug','description','image','start_at','batch_time','language','meta_data']
class OurStudentsForm(forms.ModelForm):
    class Meta:
        model = OurStudents
        fields = ['name','designation','photo','slug','batch']   
                
class CourseSubjectOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        
        if course:
            course_subjects = CourseSubject.objects.filter(course=course).order_by('order')
            existing_subject_ids = set()

            # Add existing course subjects to the form
            for cs_index, cs in enumerate(course_subjects, start=1):
                self.fields[f'order_{cs.id}'] = forms.IntegerField(
                    initial=cs.order,
                    label=f'{cs.subject.name}',
                    widget=forms.HiddenInput
                )
                existing_subject_ids.add(cs.subject.id)

            # Add new subjects not yet associated with the course
            all_subjects = course.subjects.all()  # Assuming 'subjects' is a related field in Course model
            new_subject_index = len(course_subjects) + 1  # Start new subjects after existing ones

            for subject_index, subject in enumerate(all_subjects, start=new_subject_index):
                if subject.id not in existing_subject_ids:
                    self.fields[f'order_new_{subject.id}'] = forms.IntegerField(
                        label=f'{subject.name}',
                        initial=subject_index,  # Set initial order based on index
                        widget=forms.HiddenInput
                    )