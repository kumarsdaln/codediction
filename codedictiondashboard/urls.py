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

urlpatterns = [
    path('', Views.index, name='app.dashboard'),
    path('blog/', include(
        [
            path('', BlogViews.as_view(), name='app.dashboard.blog'),
            path('add/', AddBlogViews.as_view(), name='app.dashboard.blog.add'),
            path('edit/<int:blog_id>/', EditBlogViews.as_view(), name='app.dashboard.blog.edit'),
            path('view/<slug:slug>/', BlogDetailViews.as_view(), name='app.dashboard.blog.view'),
            path('delete/<int:blog_id>/', DeleteBlogViews.as_view(), name='app.dashboard.blog.delete'),
            path('status/<int:blog_id>/', StatusBlogViews.as_view(), name='app.dashboard.blog.status'),
            path('category/', include(
                [
                    path('', BlogCategoryViews.as_view(), name='app.dashboard.blog.category'),
                    path('add/', AddBlogCategoryViews.as_view(), name='app.dashboard.blog.category.add'),
                    path('edit/<int:category_id>', EditBlogCategoryViews.as_view(), name='app.dashboard.blog.category.edit'),
                    path('delete/<int:category_id>/', DeleteBlogCategoryViews.as_view(), name='app.dashboard.blog.category.delete'),
                ]
            )),
            path('filter-by/', include(
                [
                    path('category/<slug:category_slug>/', BlogByCategoryView.as_view(), name='app.dashboard.blog.bycategory'),
                    path('status/<str:status>/', BlogByStatusView.as_view(), name='app.dashboard.blog.bystatus'),
                ]
            )),
        ]
    )),
    path('services/', include(
        [
            path('', ServicesViews.as_view(), name='app.dashboard.services'),
            path('add/', AddServicesViews.as_view(), name='app.dashboard.services.add'),
            path('edit/<int:service_id>/', EditServicesViews.as_view(), name='app.dashboard.services.edit'),
            path('view/<slug:slug>/', ServicesDetailViews.as_view(), name='app.dashboard.services.view'),
            path('delete/<int:service_id>/', DeleteServicesViews.as_view(), name='app.dashboard.services.delete'),
            path('status/<int:service_id>/', StatusServicesViews.as_view(), name='app.dashboard.services.status'),
        ]
    )),
    path('courses/', include(
        [
            path('', CoursesViews.as_view(), name='app.dashboard.courses'),
            path('add/', AddCoursesViews.as_view(), name='app.dashboard.courses.add'),
            path('edit/<int:course_id>/', EditCoursesViews.as_view(), name='app.dashboard.courses.edit'),
            path('details/<slug:slug>/', CoursesDetailViews.as_view(), name='app.dashboard.courses.view'),
            path('details/<slug:slug>/curriculum/', CoursesCurriculumViews.as_view(), name='app.dashboard.courses.curriculum'),
            path('delete/<int:course_id>/', DeleteCoursesViews.as_view(), name='app.dashboard.courses.delete'),
            path('subjects/', include(
                [
                    path('', SubjectsViews.as_view(), name='app.dashboard.courses.subjects'),
                    path('add/', AddSubjectsViews.as_view(), name='app.dashboard.courses.subjects.add'),
                    path('edit/<int:subject_id>', EditSubjectsViews.as_view(), name='app.dashboard.courses.subjects.edit'),
                    path('details/<slug:slug>/', SubjectsDetailViews.as_view(), name='app.dashboard.courses.subjects.view'),
                    path('type/', include(
                        [
                            path('', SubjectTypeViews.as_view(), name='app.dashboard.courses.subjects.type'),
                            path('add/', AddSubjectTypeViews.as_view(), name='app.dashboard.courses.subjects.type.add'),
                            path('edit/<int:subject_type_id>', EditSubjectTypeViews.as_view(), name='app.dashboard.courses.subjects.type.edit'),
                            path('delete/<int:subject_type_id>', DeleteSubjectTypeViews.as_view(), name='app.dashboard.courses.subjects.type.delete'),
                        ]
                    )),
                    path('curriculum/<slug:slug>/', include(
                        [ 
                            path('', CurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum'),
                            path('details/<slug:curriculum_slug>/', CurriculumDetailViews.as_view(), name='app.dashboard.courses.subjects.curriculum.details'),
                            path('add/', AddCurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum.add'),
                            path('<slug:rel_cur_slug>/add/', AddRelCurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum.rel.add'),
                            path('edit/<slug:curriculum_slug>', EditCurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum.edit'),
                            path('delete/<int:subject_type_id>', DeleteCurriculumViews.as_view(), name='app.dashboard.courses.subjects.curriculum.delete'),
                        ]
                    )),
                ]
            )),
            path('category/', include(
                [
                    path('', CourseCategoriesViews.as_view(), name='app.dashboard.courses.category'),
                    path('add/', AddCourseCategoriesViews.as_view(), name='app.dashboard.courses.category.add'),
                    path('edit/<int:category_id>', EditCourseCategoriesViews.as_view(), name='app.dashboard.courses.category.edit'),
                    path('delete/<int:category_id>/', DeleteCourseCategoriesViews.as_view(), name='app.dashboard.courses.category.delete'),
                ]
            )),
            path('batches/', include(
                [
                    path('', OurBatchViews.as_view(), name='app.dashboard.courses.batches'),
                    path('add/', AddOurBatchViews.as_view(), name='app.dashboard.courses.batches.add'),
                    path('edit/<int:batch_id>', EditOurBatchViews.as_view(), name='app.dashboard.courses.batches.edit'),
                    path('details/<slug:slug>/', OurBatchDetailViews.as_view(), name='app.dashboard.courses.batches.view'),
                    path('delete/<int:batch_id>/', DeleteOurBatchViews.as_view(), name='app.dashboard.courses.batches.delete'),
                ]
            )),
        ]
    )),
    path('login/', LoginViews.as_view(), name='app.dashboard.login'),
    path('logout/', LogoutViews.as_view(), name='app.dashboard.logout'),
]