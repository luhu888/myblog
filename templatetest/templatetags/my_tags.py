from django import template
from django.utils.safestring import mark_safe

register = template.Library()  # register的名字是固定的,不可改变


@register.filter
def filter_multi(v1):
    """
    不带参数的自定义过滤器
    :param v1:
    :return:
    """
    return v1+'合并'


@register.filter
def filter_multi1(v1, v2):
    """
    带参数的自定义过滤器
    :param v1:
    :return:
    """
    return v1 + v2


@register.simple_tag  # 和自定义filter类似，只不过接收更灵活的参数，没有个数限制。
def simple_tag_multi(v1, v2):
    return v1 * v2


@register.simple_tag
def my_input(id, arg):
    result = "<input type='text' id='%s' class='%s' />" % (id, arg,)
    return mark_safe(result)

