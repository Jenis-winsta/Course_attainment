# your_app/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='get_co_pso_ids')
def get_co_pso_ids(pso_co_connections, co_id):
    for co, pso_ids in pso_co_connections:
        if co == co_id:
            return pso_ids
    return []
