import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def md2html(value):
    """
    blog.content(str) to markdown string
    """
    return mark_safe(markdown.markdown(value, extensions=["fenced_code"]))
