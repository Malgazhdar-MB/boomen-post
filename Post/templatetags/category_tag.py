from django import template
from Post.views import Category


register = template.Library()

@register.simple_tag()
def get_category():
    return Category.objects.all()
