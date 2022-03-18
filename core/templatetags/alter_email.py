from django import template

register = template.Library()


@register.filter
def alter_email(value):
    return value.replace("@", "[at]")
