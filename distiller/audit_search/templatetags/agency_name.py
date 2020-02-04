from django.template import Library, Node

from distiller.data import constants

register = Library()


@register.filter
def agency_name(agency_prefix: str):
    return ', '.join(constants.AGENCIES_BY_PREFIX[agency_prefix])
