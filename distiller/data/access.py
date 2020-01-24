"""
Data access interface for external data sources used by this project.
"""

from dataclasses import dataclass
from datetime import date
from functools import reduce
from typing import Dict, List, Optional

from django.core.paginator import Paginator
from django.db.models import Q

from . import models


@dataclass
class AuditSearch:
    page: int
    page_count: int
    paginate_by: int
    cfda_num: str
    start_date: date
    end_date: date
    results: List[Dict]


def get_audit(audit_id: int):
    return {
        'audit_id': audit_id
    }


def filter_audits(
    cfda_nums: List[str],
    start_date: date,
    end_date: date,
    page: int,
    paginate_by: int = 25,
) -> AuditSearch:
    """
    Return audit search results
    """

    q_obj = Q()
    if start_date:
        q_obj &= Q(fac_accepted_date__gte=start_date)
    if end_date:
        q_obj &= Q(fac_accepted_date__lte=end_date)
    if cfda_nums:
        q_obj &= Q(cfda__cfda__in=cfda_nums)

    audits = models.Audit.objects.filter(q_obj).order_by('fac_accepted_date')

    return Paginator(audits, paginate_by).get_page(page or 1)


def get_audits_by_subagency(
    sub_agency: str,
    audit_year: Optional[int],
    start_date: date,
    end_date: date,
    page: int
):
    # Get CFDA numbers for the given sub-agency name.
    cfda_nums = models.AssistanceListing.objects.get_cfda_nums_for_agency(
        sub_agency
    )

    # Get the (audit_year, dbkey) pairs for all audits matching our search
    # criteria.
    audit_keys = models.CFDA.objects.filter(
        cfda__in=cfda_nums).values('audit_year', 'dbkey')

    # Initialize Q object with and OR of all (audit_year, dbkey) pairs.
    q_obj = reduce(lambda q_obj, keys: q_obj | Q(**keys), audit_keys, Q())

    # Filter by dates
    if audit_year:
        q_obj &= Q(audit_year=audit_year)
    if start_date:
        q_obj &= Q(fac_accepted_date__gte=start_date)
    if end_date:
        q_obj &= Q(fac_accepted_date__lte=end_date)

    audits = models.Audit.objects.filter(q_obj).order_by(
        '-audit_year', '-fac_accepted_date'
    ).prefetch_related('findings')

    return Paginator(audits, 25).get_page(page or 1)


    # # Since we don't have this in the database yet, return mock data
    # return AuditSearch(
    #     page=page,
    #     page_count=page,
    #     paginate_by=paginate_by,
    #     cfda_num=cfda_num,
    #     start_date=start_date,
    #     end_date=end_date,
    #     results=[{
    #         'audit_num': '012345',
    #         'grantee_name': 'Grantee One',
    #         'findings': [{
    #             'text': 'Finding text for 012345 #1'
    #         }, {
    #             'text': 'Finding text for 012345 #1'
    #         }],
    #         'cognizant_agency': None,
    #         # Corrective action plan text (CAP)
    #         'corrective_action_text': 'Corrective action plan text (CAP)',
    #         'repeat_findings': False,
    #         'form_url': 'http://data.gov/form1.xlsx',
    #         'report_url': 'http://data.gov/report1.pdf',
    #     }, {
    #         'audit_num': '543210',
    #         'grantee_name': 'Grantee Two',
    #         'findings': [],
    #         'cognizant_agency': None,
    #         # Corrective action plan text (CAP)
    #         'corrective_action_text': 'Corrective action plan text (CAP)',
    #         'repeat_findings': False,
    #         'form_url': 'http://data.gov/form2.xlsx',
    #         'report_url': 'http://data.gov/report2.pdf',
    #     }]
    # )
