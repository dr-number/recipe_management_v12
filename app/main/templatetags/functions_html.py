from django import template

register = template.Library()

@register.filter
def type_text(user):
    return user.get_type_text()
