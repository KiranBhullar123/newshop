import datetime

from django import template

from newshopapp.models import Category

register = template.Library()


@register.simple_tag
def current_time():
    return datetime.datetime.now()

@register.inclusion_tag('fetchcategories.html')
def fetch_categories():
    queryset = Category.objects.all()
    return {"categories":queryset}