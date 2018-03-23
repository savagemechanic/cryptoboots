from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()

@register.simple_tag
def static_main(path):
    app_static = static('/assets/')
    return app_static + path

@register.simple_tag
def active_route(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''