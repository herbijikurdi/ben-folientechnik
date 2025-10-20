from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(int(key), 0)

@register.filter
def censor_email(email):
    if email:
        return email.replace('@', '[at]')
    return ''