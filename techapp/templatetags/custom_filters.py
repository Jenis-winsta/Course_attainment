# your_app/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='get_co_pso_ids')
def get_co_pso_ids(pso_co_connections, co_id):
    for co, pso_ids in pso_co_connections:
        if co == co_id:
            return pso_ids
    return []

@register.filter(name='get_co_po_ids')
def get_co_po_ids(po_co_connections, co_id):
    for co, po_ids in po_co_connections:
        if co == co_id:
            return po_ids
    return []

@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_by_po_id')
def get_by_po_id(po_info_list, po_id):
    for po_info in po_info_list:
        if po_info['programme_outcome'].id == po_id:
            return po_info
    return None


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)
