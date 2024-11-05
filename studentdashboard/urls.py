from django.urls import path, include
from .StudentViews import Views
from .StudentViews.ProfileViews import *
from .StudentViews.RegisterViews import *
from .StudentViews.AuthViews import *
from .StudentViews.CoursesViews import *
from .StudentViews.SubjectsViews import *
from .StudentViews.CurriculumViews import *
from .StudentViews.CourseEnrollmentViews import *
from .StudentViews.SocialMediaViews import *
urlpatterns = [
    path('', Views.index, name='app.student'),
    path('profile/', include(
        [
            path('', ProfileView.as_view(), name='app.student.profile'),
            path('edit/', ProfileEditView.as_view(), name='app.student.profile.edit'),
            path('password-change/', StudentPasswordChangeView.as_view(), name='app.student.profile.password-change'),
            path('education/', EducationManageView.as_view(), name='app.student.profile.education'),
            path('education/edit/<int:pk>/', EducationManageView.as_view(), name='app.student.profile.education.edit'),
            path('education/delete/<int:pk>/', EducationManageView.as_view(), name='app.student.profile.education.delete'),
            path('social-media/', SocialMediaView.as_view(), name='app.student.profile.social-media'),
            path('social-media/<int:social_media_id>/', SocialMediaView.as_view(), name='app.student.profile.social-media'),
        ]
    )),
    path('courses/', include(
        [
            path('', CoursesViews.as_view(), name='app.student.courses'),
            path('enrolled/', EnrolledCoursesView.as_view(), name='app.student.courses.enrolled'),
            path('<slug:slug>/', CoursesDetailViews.as_view(), name='app.student.courses.view'),
            path('<slug:slug>/enroll/', CourseEnrollmentView.as_view(), name='app.student.courses.enroll'),
            path('<slug:slug>/curriculum/', CoursesCurriculumViews.as_view(), name='app.student.courses.curriculum'),
        ]
    )),
    path('subjects/', include(
        [
            path('', SubjectsViews.as_view(), name='app.student.courses.subjects'),
            path('details/<slug:slug>/', SubjectsDetailViews.as_view(), name='app.student.courses.subjects.view'),
            path('curriculum/<slug:slug>/', include(
                [ 
                    path('', CurriculumViews.as_view(), name='app.student.courses.subjects.curriculum'),
                    path('details/<slug:curriculum_slug>/', CurriculumDetailViews.as_view(), name='app.student.courses.subjects.curriculum.details'),
                ]
            )),
        ]
    )),
    path('login/', LoginViews.as_view(), name='app.student.login'),
    path('register/', RegisterView.as_view(), name='app.student.register'),
    path('logout/', LogoutViews.as_view(), name='app.student.logout'),
]