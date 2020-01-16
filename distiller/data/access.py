"""
Data access interface for external data sources used by this project.
"""

from dataclasses import dataclass
from datetime import date
from typing import Dict, List


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
    cfda_num: str,
    start_date: date,
    end_date: date,
    page: int,
    paginate_by: int = 25,
) -> AuditSearch:
    """
    Return audit search results
    """

    # Since we don't have this in the database yet, return mock data
    return AuditSearch(
        page=page,
        page_count=page,
        paginate_by=paginate_by,
        cfda_num=cfda_num,
        start_date=start_date,
        end_date=end_date,
        results=[{
            'audit_num': '012345',
            'grantee_name': 'Grantee One',
            'findings': [{
                'text': 'Finding text for 012345 #1'
            }, {
                'text': 'Finding text for 012345 #1'
            }],
            'cognizant_agency': None,
            # Corrective action plan text (CAP)
            'corrective_action_text': 'Corrective action plan text (CAP)',
            'repeat_findings': False,
            'form_url': 'http://data.gov/form1.xlsx',
            'report_url': 'http://data.gov/report1.pdf',
        }, {
            'audit_num': '543210',
            'grantee_name': 'Grantee Two',
            'findings': [],
            'cognizant_agency': None,
            # Corrective action plan text (CAP)
            'corrective_action_text': 'Corrective action plan text (CAP)',
            'repeat_findings': False,
            'form_url': 'http://data.gov/form2.xlsx',
            'report_url': 'http://data.gov/report2.pdf',
        }]
    )
