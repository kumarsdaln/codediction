from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.contrib.auth.models import User
from codedictionapp.models import UserType, StudentProfile, TeacherProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_type = UserType.objects.create(user=instance, user_type=instance.user_type)
        if instance.user_type == 'S':
            StudentProfile.objects.create(user_type=user_type)
        elif instance.user_type == 'T':
            TeacherProfile.objects.create(user_type=user_type)

        try:
            user_type = instance.user_type.user_type
            if user_type == 'S':
                group = Group.objects.get(name='Student')
            elif user_type == 'T':
                group = Group.objects.get(name='Teacher')
            instance.groups.add(group)
        except UserType.DoesNotExist:
            pass    
