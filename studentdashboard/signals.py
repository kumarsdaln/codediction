from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.contrib.auth.models import User
from studentdashboard.models import StudentProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)
        try:
            group = Group.objects.get(name='Student')
            instance.groups.add(group)
        except Group.DoesNotExist:
            pass    
