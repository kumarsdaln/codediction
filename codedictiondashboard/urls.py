from django.urls import path, include
from .DashViews import Views
from .DashViews.BlogViews import *
from .DashViews.BlogCategoryViews import *
from .DashViews.ServicesViews import *
from .DashViews.AuthViews import *
from .DashViews.SubjectTypeViews import *
from .DashViews.SubjectsViews import *
from .DashViews.CourseCategoriesViews import *
from .DashViews.CoursesViews import *
from .DashViews.CurriculumViews import *
from .DashViews.OurBatchViews import *
from .DashViews.ProfileViews import *
from .DashViews.SocialMediaPlatformViews import *
from .DashViews.StudentViews import *
urlpatterns = [
    path('', Views.index, name='app.dashboard'),
    path('blog/', include(
        [
            path('', BlogViews.as_view(), name='app.dashboard.blog'),
            path('category/', include(
                [
                    path('', BlogCategoryViews.as_view(), name='app.dashboard.blog.category'),
                    path('add/', AddBlogCategoryViews.as_view(), name='app.dashboard.blog.category.add'),
                    path('<int:category_id>/edit/', EditBlogCategoryViews.as_view(), name='app.dashboard.blog.category.edit'),
                    path('<int:category_id>/delete/', DeleteBlogCategoryViews.as_view(), name='app.dashboard.blog.category.delete'),
                ]
            )),
            path('add/', AddBlogViews.as_view(), name='app.dashboard.blog.add'),
            path('<slug:slug>/', BlogDetailViews.as_view(), name='app.dashboard.blog.view'),
            path('<int:blog_id>/edit/', EditBlogViews.as_view(), name='app.dashboard.blog.edit'),
            path('<int:blog_id>/delete/', DeleteBlogViews.as_view(), name='app.dashboard.blog.delete'),
            path('<int:blog_id>/status/', StatusBlogViews.as_view(), name='app.dashboard.blog.status'),
            
        ]
    )),
    path('services/', include(
        [
            path('', ServicesViews.as_view(), name='app.dashboard.services'),
            path('add/', AddServicesViews.as_view(), name='app.dashboard.services.add'),
            path('<slug:slug>/', ServicesDetailViews.as_view(), name='app.dashboard.services.view'),
            path('<int:service_id>/edit/', EditServicesViews.as_view(), name='app.dashboard.services.edit'),
            path('<int:service_id>/delete/', DeleteServicesViews.as_view(), name='app.dashboard.services.delete'),
            path('<int:service_id>/status/', StatusServicesViews.as_view(), name='app.dashboard.services.status'),
        ]
    )),
    path('courses/', include(
        [
            path('', CoursesViews.as_view(), name='app.dashboard.courses'),
            path('category/', include(
                [
                    path('', CourseCategoriesViews.as_view(), name='app.dashboard.courses.category'),
                    path('add/', AddCourseCategoriesViews.as_view(), name='app.dashboard.courses.category.add'),
                    path('<int:category_id>/edit/', EditCourseCategoriesViews.as_view(), name='app.dashboard.courses.category.edit'),
                    path('<int:category_id>/delete/', DeleteCourseCategoriesViews.as_view(), name='app.dashboard.courses.category.delete'),
                ]
            )),
            path('add/', AddCoursesViews.as_view(), name='app.dashboard.courses.add'),
            path('<slug:slug>/', CoursesDetailViews.as_view(), name='app.dashboard.courses.view'),
            path('<slug:slug>/curriculum/', CoursesCurriculumViews.as_view(), name='app.dashboard.courses.curriculum'),
            path('<int:course_id>/status/', StatusCoursesViews.as_view(), name='app.dashboard.courses.status'),
            path('<int:course_id>/edit/', EditCoursesViews.as_view(), name='app.dashboard.courses.edit'),
            path('<int:course_id>/delete/', DeleteCoursesViews.as_view(), name='app.dashboard.courses.delete'),
        ]
    )),
    path('subjects/', include(
        [
            path('', SubjectsViews.as_view(), name='app.dashboard.courses.subjects'),
            path('type/', include(
                [
                    path('', SubjectTypeViews.as_view(), name='app.dashboard.courses.subjects.type'),
                    path('add/', AddSubjectTypeViews.as_view(), name='app.dashboard.courses.subjects.type.add'),
                    path('<int:subject_type_id>/edit/', EditSubjectTypeViews.as_view(), name='app.dashboard.courses.subjects.type.edit'),
                    path('<int:subject_type_id>/delete/', DeleteSubjectTypeViews.as_view(), name='app.dashboard.courses.subjects.type.delete'),
                ]
            )),
            path('curriculum/<slug:slug>/', include(
                [ 
                    path('', CurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum'),
                    path('add/', AddCurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum.add'),
                    path('<slug:curriculum_slug>', CurriculumDetailViews.as_view(), name='app.dashboard.courses.subjects.curriculum.details'),
                    path('<slug:rel_cur_slug>/add/', AddRelCurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum.rel.add'),
                    path('<slug:curriculum_slug>/edit/', EditCurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum.edit'),
                    path('<int:subject_type_id>/delete/', DeleteCurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum.delete'),
                ]
            )),
            path('add/', AddSubjectsViews.as_view(), name='app.dashboard.courses.subjects.add'),
            path('<slug:slug>/', SubjectsDetailViews.as_view(), name='app.dashboard.courses.subjects.view'),
            path('<slug:slug>/update-order', UpdateCurriculumOrderViews.as_view(), name='app.dashboard.courses.subjects.update-order'),
            path('<int:subject_id>/edit/', EditSubjectsViews.as_view(), name='app.dashboard.courses.subjects.edit'),
        ]
    )),
    path('batches/', include(
        [
            path('', OurBatchViews.as_view(), name='app.dashboard.courses.batches'),
            path('add/', AddOurBatchViews.as_view(), name='app.dashboard.courses.batches.add'),
            path('<slug:slug>/', OurBatchDetailViews.as_view(), name='app.dashboard.courses.batches.view'),
            path('<int:batch_id>/edit/', EditOurBatchViews.as_view(), name='app.dashboard.courses.batches.edit'),
            path('<int:batch_id>/delete/', DeleteOurBatchViews.as_view(), name='app.dashboard.courses.batches.delete'),
        ]
    )),
    path('students/', include(
        [
            path('', StudentViews.as_view(), name='app.dashboard.students'),
            # path('add/', AddServicesViews.as_view(), name='app.dashboard.students.add'),
            path('<int:pk>/', StudentDetailViews.as_view(), name='app.dashboard.students.view'),
            path('<int:student_id>/edit/', EditStudentViews.as_view(), name='app.dashboard.students.edit'),
            path('<int:student_id>/password-change/', StudentPasswordChangeView.as_view(), name='app.dashboard.students.password-change'),
            path('<int:student_id>/education/', StudentEducationManageView.as_view(), name='app.dashboard.students.education'),
            path('<int:student_id>/education/edit/<int:pk>/', StudentEducationManageView.as_view(), name='app.dashboard.students.education.edit'),
            path('<int:student_id>/education/delete/<int:pk>/', StudentEducationManageView.as_view(), name='app.dashboard.students.education.delete'),
            path('<int:user_id>/status/', StatusStudentViews.as_view(), name='app.dashboard.students.status'),
        ]
    )),
    path('social-media-platform/', SocialMediaPlatformManageView.as_view(), name='app.dashboard.social-media-platform'),
    path('social-media-platform/<int:platform_id>/', SocialMediaPlatformManageView.as_view(), name='app.dashboard.social-media-platform'),
    path('profile/', include(
        [
            path('', ProfileView.as_view(), name='app.dashboard.profile'),
        ]
    )),
    path('login/', LoginViews.as_view(), name='app.dashboard.login'),
    path('logout/', LogoutViews.as_view(), name='app.dashboard.logout'),
]