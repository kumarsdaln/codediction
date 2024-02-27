from django import forms
from codedictionapp.models import *
import datetime

class ContactusForm(forms.ModelForm):
    class Meta:
        model = Contactus
        fields = ['name', 'email', 'phone', 'subject', 'message']
    def save(self, commit=True):
        instance = super().save(commit=False)  # Don't save to database yet
        instance.uploaded_at=datetime.datetime.now()
        if commit:
            instance.save()  # Save to database if commit is True
        return instance        

class SubscribeNewsletterForm(forms.ModelForm):
    class Meta:
        model = SubscribeNewsletter
        fields = ['email']
    def save(self, commit=True):
        instance = super().save(commit=False)  # Don't save to database yet
        instance.uploaded_at=datetime.datetime.now()
        if commit:
            instance.save()  # Save to database if commit is True
        return instance    