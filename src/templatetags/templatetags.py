from django import template

register = template.Library()


# @register.simple_tag()
# def try_or(function, default=None, expected_exceptions=(Exception,)):
#     try:
#         return function()
#     except expected_exceptions:
#         return default

@register.simple_tag()
def take_image_url(image_object, default="", expected_exceptions=(Exception,)):
    try:
        return image_object.url
    except expected_exceptions:
        return default