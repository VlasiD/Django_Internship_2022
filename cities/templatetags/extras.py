from django import template
register = template.Library()


@register.filter()
def image_tag(param):
    if param:
        return "/media/done.svg"
    else:
        return "/media/unavailable.svg"


@register.filter()
def get_item(dictionary, key):
    return dictionary.get(key)