from django import template
from app import settings

register = template.Library()

@register.filter
def get_const(text):
    return getattr(settings, text, '')
