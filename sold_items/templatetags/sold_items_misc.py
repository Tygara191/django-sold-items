from django import template
from sold_items.common import is_int

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(1, number+1)

@register.simple_tag(name='listing_urlparams', takes_context=True)
def listing_urlparams(context, number):
    request = context['request']
    request.GET._mutable = True
    request.GET['page'] = number
    return "?" + request.GET.urlencode()

@register.simple_tag(name="auto_value", takes_context=True)
def auto_value(context, key):
    request = context['request']
    if(request.GET.get(key)):
        return 'value="%s"' % request.GET.get(key)
    return ""

@register.simple_tag(name="auto_selected_option", takes_context=True)
def auto_selected_option(context, key, value):
    request = context['request']
    if request.GET.get(key):
        try:
            if is_int(value):
                if int(request.GET.get(key)) == int(value):
                    return "selected"
            else:
                if request.GET.get(key) == value:
                    return "selected"
        except ValueError:
            return ""
    return ""


@register.simple_tag(name="auto_checked", takes_context=True)
def auto_checked(context, key, value):
    request = context['request']
    if request.GET.get(key):
        args = request.GET.get(key).split(',')
        if str(value) in args:
            return "checked"
    return ""

@register.simple_tag(name="auto_checked_simple", takes_context=True)
def auto_checked_simple(context, key):
    request = context['request']
    if request.GET.get(key):
        return "checked"
    return ""

@register.simple_tag(name='percentage')
def percentage(new_price, old_price):
    j = old_price - new_price
    return int(round(j / old_price * 100, 2))