"""
Tests for the load of FAC tables.
"""

import datetime
import os

from ..etls.load_dumps import parse_findings_text_csv

DATA_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.join('data'))
)
TEST_FINDINGS_TEXT_PATH = os.path.join(
    DATA_PATH, os.path.join('sample_findings_text.txt')
)


def test_findings_text_parser():
    results = parse_findings_text_csv(open(TEST_FINDINGS_TEXT_PATH))
    assert list(results) == [
        {
            'SEQ_NUMBER': '21',
            'DBKEY': '66846',
            'AUDITYEAR': '2019',
            'FINDINGREFNUMS': '2019-001',
            'CHARTSTABLES': 'N',
            'TEXT': 'Health Center Program Cluster –\nCFDA Nos. 93.224 and 93.527\nU.S. Department of Health and Human Services\nAward No. 6 H80CS00671-18-24\nProgram Year 2019\nCriteria or Specific Requirement – Special Tests and Provisions: Sliding Fee\nDiscounts (42 USC 254(k)(3)(g); 42 CFR sections 51c.303(g); and 42 CFR\nsections 56.303 (f))\nConditions – Patients received a sliding fee discount that was consistent with\nthe stated sliding fee discount categories under the Organization’s policy,\nhowever the policy was not in compliance with regulations concerning\ndiscounts provided based upon graduations of income for dental services.\nQuestioned cost – None\nContext – A sample of 25 patients were tested out of the total population of\n97,199 encounters. The sampling methodology used is not and is not intended\nto be statistically valid. Six patients received a sliding fee adjustment that\nwas consistent with the approved policy for the sliding fee adjustments based\non their income documentation however the policy was not compliant with\nthe federal program requirements.\nEffect – Sliding fee discounts were given to patients that were inconsistent\nwith the federal regulation for the sliding fee discount policy.\nCause – The Organization’s sliding fee policy did not comply with the Health\nCenter Program Compliance Manual for certain dental services.\nIdentified as a repeat finding, if applicable – Not a repeat finding.\nRecommendation – We recommend management continue to ensure all\npersonnel understand the sliding fee scale policy and adhere to the\nrequirements and guidelines set forth in the policy. Procedures should be\nimplemented to ensure that eligible patients receive discounts in accordance\nwith the sliding fee scale and the Health Center Program Compliance\nManual.                 Views of Responsible Officials and Planned Corrective Action – Northwest\nHealth Services, Inc. is reviewing current Sliding Fee Scale Discount\nprogram policy and procedures and will make the necessary updates to assure\ncompliance with the Health Center Program Compliance Manual. By\nJuly 31, 2019, we will have the policy and procedures updated, implemented\nand staff trained. The CFO and CEO will be responsible for ensuring this\nmatter is done.',
        },
        {
            'SEQ_NUMBER': '61',
            'DBKEY': '230559',
            'AUDITYEAR': '2019',
            'FINDINGREFNUMS': '2019-001',
            'CHARTSTABLES': 'N',
            'TEXT': 'PREVIOUSLY REPORTED ITEMS NOT RESOLVED\n\nFinding 2019-001\n\nCriteria:\nGenerally, a system of internal control contemplates separation of duties such that no individual has responsibility to execute a transaction, have physical access to the related assets, and have responsibility or authority to record the transactions.\n\nCondition:\nDue to the limited size of the Cooperative’s business staff, the Cooperative has limited segregation of duties.\n\nQuestioned Costs:\nNone.\n\nContext:\nThe Cooperative has informed us that the small size of its business office staff precludes proper separation of duties at this time.\n\nEffect:\nThe Cooperative is unable to maintain separation of incompatible duties.\n\nCause:\nLimited number of staff in the business office.\n\nRecommendation:\nWe recommend that the Cooperative continue to separate incompatible duties as best it can within the limits of what the Cooperative considers to be cost beneficial.\n\nCurrent Status:\nUnresolved, the Cooperative still has a limited number of staff in the business office.\n\nAction Taken:\nThe Cooperative reviews and makes improvements to its internal controls on an ongoing basis, and attempts to maximize the segregation of duties in all areas within the limits of the staff available.\n\nViews of Responsible Officials and Planned Corrective Actions:\nThe Cooperative agrees with this finding and will adhere to the corrective action plan on page 27 in this audit report.',
        },
        {
            'SEQ_NUMBER': '62',
            'DBKEY': '230559',
            'AUDITYEAR': '2019',
            'FINDINGREFNUMS': '2019-002',
            'CHARTSTABLES': 'N',
            'TEXT': 'SECTION II  FINDINGS – FINANCIAL STATEMENTS AUDIT (continued)\n\nPREVIOUSLY REPORTED ITEMS NOT RESOLVED (continued)\n\nFinding 2019-002\n\nCriteria:\nGenerally, a system of internal control includes the ability to understand and prepare the Cooperative’s financial statements and related disclosures in accordance with accounting principles generally accepted in the United States of America (GAAP).\n\nCondition:\nDue to the limited size of the Cooperative’s business staff and related resources available, the Cooperative has utilized the auditors experience to assist with adjusting journal entries and preparing the financial statements and related disclosures in accordance with accounting principles generally accepted in the United States of America.\n\nQuestioned Costs:\nNone.\n\nContext:\nThe Cooperative has informed us that the small size and qualifications of its business office staff precludes the Cooperative from posting adjusting journal entries and preparing its own financial statements.\n\nEffect:\nThe Cooperative is utilizes the auditor to prepare GAAP based financial statements.\n\nCause:\nLimited number of staff and hours available preclude the Cooperative from preparing the GAAP based financial statements. The Cooperative will continue to review auditor prepared financial statements.\n\nRecommendation:\nWe recommend that the Cooperative continue to review the auditor prepared adjusting journal entries and financial statements with the intention of understanding and acceptance of responsibility for reporting under generally accepted accounting principles.\n\nCurrent Status:\nUnresolved, the number of staff and qualifications of staff have not changed. The Cooperative is continuing to review the auditor prepared adjusting journal entries and financial statements.\n\nAction Taken:\nThe Cooperative will continue to review the auditor prepared adjusting journal entries and financial statements with the intention of understanding and acceptance of responsibility for reporting under generally accepted accounting principles.\n\nViews of Responsible Officials and Planned Corrective Actions:\nThe Cooperative agrees with this finding and will adhere to the corrective action plan on page 27 in this audit report.\n\n',
        },
    ]
