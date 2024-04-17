from django.urls import path, include
from . import views
from .import fetch
from .AppViews.ContactusViews import *
from .AppViews.SubscribeViews import *
urlpatterns = [
    path("", views.index, name="app.index"),
    path("services/", include(
        [
            path("", views.services, name="app.services"),
            path("<slug:service_slug>", views.serviceDetails, name="app.services.details"),
        ]
    )),
    path("courses/", include(
        [
            path("", views.courses, name="app.courses"),
            path("<str:category_slug>/", views.coursesByCategroy, name="app.courses.bycategory"),
            path("<str:category_slug>/<str:course_slug>/", views.courseDetails, name="app.courses.details"),
            path("fetch/", include(
                [
                    path("curriculum/<int:subject_id>/", fetch.fetchCurriculum, name="app.courses.fetch.curriculum"),
                    path("subtopics/<int:topic_id>/", fetch.fetchSubtopics, name="app.courses.fetch.subtopics"),
                ]
            )),
            
        ]
    )),
    path("batches/", include(
        [
            path("<slug:batch_slug>/", views.batchDetails, name="app.batches.details"),
        ]
    )),
    path("projects/", include(
        [
            path("", views.projects, name="app.projects"),
            path("<str:category_slug>/", views.projectsByCategroy, name="app.project-by-category"),
            path("<str:category_slug>/<str:project_slug>/", views.projectsDetails, name="app.projects.details"),
        ]
    )),

    path("blog/", include(
        [
            path("", views.blog, name="app.blog"),
            path("<str:category_slug>/", views.blogByCategory, name="app.blog.bycategory"),
            path('<str:category_slug>/<str:blog_slug>/', views.blogDetails, name='app.blog.details'),

        ]
    )),


    path("questions/", views.question, name="app.questions"),
    path("questions/<str:question_link>/", views.answer, name="app.questions.answers"),
    
    path("learn/<str:link_url>/", views.subjectDetails, name="app.subject"),
    

    
    path("maintaince/", views.maintainance, name="app.maintainance"),
    path("index-2/", views.index2, name="app.index-2"),
    path("index-3/", views.index3, name="app.index-3"),
    path("about/", views.about, name="app.about"),
    path("contact/", views.contact, name="app.contact"),
    path("contact/sendform/", AddContactusViews.as_view(),name="app.contact.sendform"),
    path("newsletter/sendform/", AddSubscribeViews.as_view(),name="app.newsletter.sendform"),

    path("portfolio/", views.portfolio, name="app.portfolio"),
    path("portfolio-detail/", views.portfolioDetails, name="app.portfolio-detail"),
    
    
    path("mentors/", views.mentors, name="app.mentors"),
    path("mentor-detail/", views.mentorDetails, name="app.mentor-detail"),
    path("price/", views.price, name="app.price"),
    path("faq/", views.faq, name="app.faq"),
]