from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import *



def index(request):
    subjects = Subjects.objects.all()
    courses = Courses.objects.all()[:2]
    services = Services.objects.all()
    batches = OurBatch.objects.filter(status="u")
    projects = OurWork.objects.filter()
    blog = Blog.objects.order_by('-id')[:5]
    subjects = Subjects.objects.all()[:8]
    team = OurTeam.objects.all()[:5]
    testimonial = Testimonial.objects.all()[:5]
    clients = OurClients.objects.all()[:5]
    return render(request, "courses/index.html", {
        'subjects':subjects,
        'courses':courses,
        'services':services,
        'batches':batches,
        'projects':projects,
        'blog_list':blog,
        'subjects':subjects,
        'team':team,
        'testimonial':testimonial,
        'clients':clients
    })

def courses(request):
    courses = Courses.objects.all()
    courses_categories = CourseCategories.objects.all()
    subjects = Subjects.objects.all()
    if courses!=None:
        return render(request, "courses/courses.html", {
            'courses':courses,
            'courses_categories':courses_categories,
            'subjects':subjects
        })
    else:
         return render(request, "courses/404.html")
    
def coursesByCategroy(request, category_link):
    courses = CourseCategories.objects.get(link_url=category_link).courses_set.all()
    courses_categories = CourseCategories.objects.all()
    subjects = Subjects.objects.all()
    if courses!=None:
        return render(request, "courses/courses.html", {
            'courses':courses,
            'courses_categories':courses_categories,
            'subjects':subjects
        })
    else:
         return render(request, "courses/404.html")

def courseDetails(request, category_slug, course_slug):
    courses = Courses.objects.all()
    course = Courses.objects.get(slug=course_slug)
    courses_categories = CourseCategories.objects.all()
    course_time = 0
    course_price = 0
    if course != None:
        for subject in course.subjects.all():
            course_time = course_time + subject.time_period
            course_price = course_price + subject.price
        return render(request, "courses/course-detail.html", {
            'course':course,
            'course_time':course_time,
            'course_price':course_price,
            'courses_categories':courses_categories,
            'courses':courses
        })
    else:
        return render(request, "courses/404.html")
    
def batchDetails(request, batch_slug):
    batch = OurBatch.objects.get(slug=batch_slug)
    if batch != None:
        return render(request, "courses/batch-details.html", {
            'batch':batch,
        })
    else:
        return render(request, "courses/404.html")
    

        
def consultation(request):
    return render(request, "courses/consultation.html")   

def webinars(request):
    return render(request, "courses/webinars.html")   

def question(request):
    questions = Question.objects.all()
    courses = Courses.objects.all()[:4]
    return render(request, "courses/question.html", {
        'questions':questions,
        'courses':courses
    })

def answer(request, question_link):
    question = Question.objects.get(link_url=question_link)
    return render(request, "courses/answer.html", {
        'question':question
    })

def subjectDetails(request, link_url):
    try:
        subjects = Subjects.objects.get(link_url=link_url)
        curriculum_list = subjects.curriculum_set.select_related('relation_with').filter(relation_with=None)
        all_subjects = Subjects.objects.all()
   
        return render(request, "courses/subject-detail.html", {
            'subjects': subjects,
            'curriculum_list': curriculum_list,
            'all_subjects':all_subjects
        })
        
    except Subjects.DoesNotExist:
        return render(request, "courses/404.html")


def fetch_all_blogs(request):
    try:
        blogs = Blog.objects.select_related('category', 'uploaded_by').all()
        limit = 10
        paginator = Paginator(blogs, limit)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        blog_categories = BlogCategory.objects.all()
        if len(blogs) > 1:
            pass
        else:
            page_obj = []

    except Exception as e:
        blogs = []
        page_obj = []

    return render(request, "courses/blog.html", {"blogs": blogs, "page_obj": page_obj, "blog_categories":blog_categories})


def blog(request):
    return fetch_all_blogs(request)

def blogByCategory(request, category_slug):
    try:
        blog_category = get_object_or_404(BlogCategory, slug=category_slug)
    except Exception as e:
        return render(request, "courses/404.html")

    blogs = BlogCategory.objects.get(slug=category_slug).blog_set.all()
    limit = 10
    paginator = Paginator(blogs, limit)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    blog_categories = BlogCategory.objects.all()
    if len(blogs) > 1:
        pass
    else:
        page_obj = []    

    return render(request, "courses/blog.html", {"blogs": blogs, "page_obj": page_obj, "blog_categories":blog_categories})

def blogDetails(request, category_slug, blog_slug):
    try:
        blog = get_object_or_404(Blog, slug=blog_slug)
    except Blog.DoesNotExist:
        return render(request, "courses/blog-not-found.html")

    category = blog.category
    related_blogs = Blog.objects.filter(
        category=category).exclude(slug=blog_slug)[:5]
    previous_blog = Blog.objects.filter(
        category=category, uploaded_at__lt=blog.uploaded_at).order_by('uploaded_at').first()
    next_blog = Blog.objects.filter(
        category=category, uploaded_at__gt=blog.uploaded_at).order_by('uploaded_at').first()
    
    blog_categories = BlogCategory.objects.all()

    context = {
        'blog': blog,
        'category': category,
        'related_blogs': related_blogs,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
        'blog_categories':blog_categories
    }

    return render(request, "courses/blog-detail.html", context)

def projects(request):
    pass

def projectsByCategroy(request):
    pass

def projectsDetails(request):
    pass

def index2(request):
    return render(request, "courses/index-2.html")

def index3(request):
    return render(request, "courses/index-3.html")

def about(request):
    team = OurTeam.objects.all()
    return render(request, "courses/about.html",
                  {
                      'team':team
                  })

def contact(request):
    form = request.GET.get('form', None)
    if form:
        msg = "Thanks for contact us we'll back to you soon..."
    else:
        msg = False    
    return render(request, "courses/contact.html", {
        'msg':msg
    })

def services(request):
    services = Services.objects.all()
    return render(request, "courses/services.html", {
        'services':services
    })

def serviceDetails(request, service_slug):
    service = Services.objects.get(slug=service_slug)
    services = Services.objects.all()
    return render(request, "courses/services-details.html", {
        'service':service,
        'services':services
    })

def portfolio(request):
    return render(request, "courses/portfolio.html")

def portfolioDetails(request):
    return render(request, "courses/portfolio-detail.html")

def mentors(request):
    return render(request, "courses/mentors.html")

def mentorDetails(request):
    return render(request, "courses/mentor-detail.html")

def price(request):
    return render(request, "courses/price.html")

def faq(request):
    return render(request, "courses/faq.html")