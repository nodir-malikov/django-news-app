from django import template
from django.core.cache import cache

from news.models import Category
from django.db.models import *

register = template.Library()


@register.simple_tag()
def get_categories():
    # return Category.objects.order_by('title')
    # categories = cache.get('categories')
    # if not categories:
    #     categories = Category.objects.filter(get_news__is_published=True).annotate(cnt=Count('get_news')).filter(
    #         cnt__gt=0)
    #     cache.set('categories', categories, 30)
    categories = Category.objects.filter(get_news__is_published=True).annotate(cnt=Count('get_news')).filter(
            cnt__gt=0)
    return categories
