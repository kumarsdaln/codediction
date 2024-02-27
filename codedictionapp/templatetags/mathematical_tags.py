from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(num_1, args):
    if args:
        num_2 = int(args)
    return num_1*num_2
@register.filter(name='subtract')
def subtract(num_1, args):
    if args:
        num_2 = int(args)
    return num_1-num_2