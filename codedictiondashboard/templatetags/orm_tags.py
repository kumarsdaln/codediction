from django import template
import json
from django.db.models import Min, Max
register = template.Library()


@register.filter(name='in_filter_by')
def in_filter_by(quesry_set, args):
    if args:
        # Decode JSON data into a Python object (dictionary in this case)
        python_obj = json.loads(args)
        # Filter queryset based on key-value pairs
        filtered_queryset = quesry_set.filter(**python_obj)
    return filtered_queryset
@register.filter(name='min_val')
def min_val(quesry_set, args):
    if args:
        filed = args
        min_value = quesry_set.aggregate(min_value=Min(filed))['min_value']
    return min_value
@register.filter(name='max_val')
def max_val(quesry_set, args):
    if args:
        filed = args
        max_value = quesry_set.aggregate(max_value=Max(filed))['max_value']
    return max_value