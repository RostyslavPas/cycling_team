from django import template
from django.urls import translate_url as django_translate_url
from django.utils.translation import gettext as _

register = template.Library()


@register.filter(name="t")
def translate_value(value):
    if value is None:
        return ""
    return _(str(value))


@register.simple_tag(takes_context=True)
def translate_url(context, lang_code):
    request = context.get("request")
    if not request:
        return ""
    return django_translate_url(request.get_full_path(), lang_code)
