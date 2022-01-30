from django import template
register = template.Library()


@register.filter()
def image_tag(param):
    if param:
        return "/media/done.svg"
    else:
        return "/media/unavailable.svg"
