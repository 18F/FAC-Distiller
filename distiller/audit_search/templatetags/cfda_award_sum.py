from django.template import Library

register = Library()


@register.filter
def cfda_award_sum(cfdas, cfda_prefixes):
    award_sum = 0
    for cfda in cfdas:
        if any(cfda.cfda_id.startswith(prefix) for prefix in cfda_prefixes):
            award_sum += cfda.amount
    return award_sum
