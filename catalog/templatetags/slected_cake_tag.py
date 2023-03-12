from django import template
from catalog.models import Cake

register = template.Library()


@register.simple_tag()
def selected_cakes():
    return Cake.objects.filter(selected=True)
