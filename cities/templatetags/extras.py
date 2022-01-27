from django import template
register = template.Library()


@register.filter()
def image_tag(param):
    if param:
        return "/media/success.png"
    else:
        return "/media/error.jpg"
