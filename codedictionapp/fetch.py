from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
import json
from django.template import loader
from django.shortcuts import render
from .models import Subjects, Courses, Curriculum


def fetchCurriculum(request, subject_id):
    subjects = Curriculum.objects.filter(subject=subject_id, relation_with=None)
    return JsonResponse(json.loads(serialize("json", subjects)), safe=False)

def fetchSubtopics(request, topic_id):
    subjects = Curriculum.objects.filter(relation_with=topic_id)
    return JsonResponse(json.loads(serialize("json", subjects)), safe=False)