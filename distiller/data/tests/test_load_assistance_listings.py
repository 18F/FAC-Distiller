"""
Tests for the load of assistance listings.
"""

import datetime
import os

from ..etls.assistance_listings import _yield_rows


def test_baseline():
    """
    Import the first ten lines of the CSV, as they exist at time of writing.
    Rather than make this an integration test dependent on the database,
    just read the data from dicts and confirm we can serialize it to known
    values.
    """

    with open(SAMPLE_CSV_PATH) as csv_file:
        assert list(_yield_rows(csv_file)) == PARSED_ROWS

    assert True


SAMPLE_CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    'data',
    'sample_assistance_listings.csv'
)

PARSED_ROWS = [
    {
        "program_title": "Agricultural Research Basic and Applied Research",
        "program_number": "10.001",
        "popular_name": "(Extramural Research)",
        "federal_agency": "AGRICULTURAL RESEARCH SERVICE, AGRICULTURE, DEPARTMENT OF",
        "authorization": {
            "list": [
                {
                    "act": {"description": "Food Security Act of 1985"},
                    "publicLaw": {"congressCode": "99", "number": "198"},
                    "USC": {"title": "7", "section": "427-427i, 1624"},
                    "authorizationTypes": {"USC": True, "act": True, "publicLaw": True},
                    "usc": {"title": "7", "section": "427-427i, 1624"},
                }
            ]
        },
        "objectives": "To make agricultural research discoveries, evaluate alternative ways of attaining research goals, and provide scientific technical information.",
        "assistance_types": "PROJECT GRANTS",
        "uses_restrictions": "Not Applicable",
        "applicant_eligibility": "Usually nonprofit institutions of higher education or other nonprofit research organizations, whose primary purpose is conducting scientific research.",
        "beneficiary_eligibility": "Usually nonprofit institutions of higher education or other nonprofit research organizations, whose primary purpose is conducting scientific research.",
        "credentials_documentation": {"isApplicable": False},
        "preapplication_coordination": {
            "environmentalImpact": {
                "reports": [{"isSelected": True, "reportCode": "otherRequired"}]
            },
            "description": "Pre-application coordination is required.",
        },
        "application_procedures": {
            "description": "Letters should be submitted to the Agricultural Research Service, Department of Agriculture. Give name of applicants, location of facilities, and State of incorporation, if any."
        },
        "award_procedure": "A peer review panel considers each proposal, evaluates the qualifications of applicants in line with research to be undertaken and determines priority for final negotiations of the grant.",
        "deadlines": {"flag": "no", "list": []},
        "approval_time": "Not Applicable",
        "appeals": "None",
        "renewals": "None",
        "requirements": {"types": {"moe": False, "formula": False, "matching": False}},
        "assistance_period": {
            "awarded": "other",
            "description": "None",
            "awardedDescription": "None",
        },
        "reports": [
            {
                "code": "program",
                "isSelected": True,
                "description": "Progress reports, final technical reports, financial statements, and inventions and subaward reports.",
            },
            {"code": "cash", "isSelected": False},
            {"code": "progress", "isSelected": False},
            {"code": "expenditure", "isSelected": False},
            {"code": "performanceMonitoring", "isSelected": False},
        ],
        "audits": {
            "isApplicable": True,
            "description": "As performed by cognizant audit agency.",
        },
        "records": "Financial records, supporting documents, statistical records, and all other records pertinent to an award shall be retained for a period of three years from the date of submission of the final expenditure report or, for awards that are renewed quarterly or annually, from the date of the submission of the quarterly or annual financial report, as authorized by the Federal awarding agency.",
        "account_identification": "12-1400-0-1-352;",
        "obligations": "(Project Grants) FY 18$6,271,318.00; FY 19 est $4,704,045.00; FY 20 est $4,713,453.00; FY 17$45,381,885.00; FY 16$45,381,885.00; - ",
        "assistance_range": "$5,000 to $50,000.  Average $20,000",
        "program_accomplishments": {"list": [], "isApplicable": False},
        "regulations": "2 CFR 200",
        "regional_local_office": {
            "flag": "appendix",
            "description": "See the Agricultural Research Service Regional Offices listed in Appendix IV of the Catalog.",
        },
        "headquarters_office": "Kathleen S. Townson,5601 Sunnyside Ave, MS-5110, Beltsville, MD 20705 Email:< a href='mailto:kathleen.townson@ars.usda.gov'>kathleen.townson@ars.usda.gov</a>Phone: (301) 504-1702.;",
        "website": "http://www.ars.usda.gov",
        "related_programs": "10.200 Grants for Agricultural Research, Special Research Grants; 10.207 Animal Health and Disease Research; 10.203 Payments to Agricultural Experiment Stations Under the Hatch Act; 10.500 Cooperative Extension Service; 10.202 Cooperative Forestry Research; 10.205 Payments to 1890 Land-Grant Colleges and Tuskegee University; 10.250 Agricultural and Rural Economic Research, Cooperative Agreements and Collaborations; 10.652 Forestry Research; 10.700 National Agricultural Library; ",
        "funded_project_examples": "Not Applicable.",
        "selection_criteria": "Peer review.",
        "published_date": datetime.date(1965, 1, 1),
        "parent_shortname": "USDA",
        "sam_gov_url": "https://beta.sam.gov/fal/7cafa05a81ad4d3597b53042add7488e/view",
        "recovery": False,
    },
    {
        "program_title": "Plant and Animal Disease, Pest Control, and Animal Care",
        "program_number": "10.025",
        "popular_name": "",
        "federal_agency": "ANIMAL AND PLANT HEALTH INSPECTION SERVICE, AGRICULTURE, DEPARTMENT OF",
        "authorization": {
            "list": [
                {
                    "act": {"description": "Plant Protection Act"},
                    "publicLaw": {"congressCode": "106", "number": "224"},
                    "USC": {"title": "7", "section": "7701-7772"},
                    "authorizationTypes": {"USC": True, "act": True, "publicLaw": True},
                    "usc": {"title": "7", "section": "7701-7772"},
                },
                {
                    "act": {"description": "Animal Welfare Act, as amended"},
                    "USC": {"title": "7", "section": "2131-2155"},
                    "authorizationTypes": {"USC": True, "act": True},
                    "usc": {"title": "7", "section": "2131-2155"},
                },
                {
                    "act": {
                        "description": "Farm Security and Rural Investment Act of 2002"
                    },
                    "publicLaw": {"congressCode": "107", "number": "171"},
                    "USC": {"title": "E", "section": "10401-10418"},
                    "authorizationTypes": {"USC": True, "act": True, "publicLaw": True},
                    "usc": {"title": "E", "section": "10401-10418"},
                },
            ]
        },
        "objectives": "To protect U.S. agriculture from economically injurious plant and animal diseases and pests, ensure the safety and potency of veterinary biologic, and ensure the humane treatment of animals.",
        "assistance_types": "PROJECT GRANTS",
        "uses_restrictions": "Not Applicable",
        "applicant_eligibility": "Foreign, State, local, and U.S. Territorial government agencies, nonprofit institutions of higher education, and nonprofit associations or organizations requiring Federal support to eradicate, control, or assess the status of injurious plant and animal diseases and pests that are a threat to regional or national agriculture and conduct related demonstration projects.",
        "beneficiary_eligibility": "Farmers, ranchers, agriculture producers, State, local, U.S. Territorial government agencies, public and private institutions and organizations benefit from Federal assistance to eradicate or control injurious plant and animal diseases and pests that are a threat to regional or national agriculture.",
        "credentials_documentation": {
            "description": "Curriculum vitae for principal investigator, except for State, local, and Territorial government cooperators.",
            "isApplicable": True,
        },
        "preapplication_coordination": {
            "environmentalImpact": {
                "reports": [
                    {"isSelected": True, "reportCode": "ExecutiveOrder12372"},
                    {"isSelected": True, "reportCode": "otherRequired"},
                ]
            },
            "description": "N/A",
        },
        "application_procedures": {
            "description": 'Comply with E.O. 12372, "Intergovernmental Review of Federal Programs," and submit a completed Standard Form 424 "Application for Federal Assistance (Non-construction)" and project proposal (work plan), financial plan, curriculum vitae, and other required certifications to the appropriate APHIS area, regional, or Headquarters Office.  See Regional and Local Office Address Listing.'
        },
        "award_procedure": "Applications are approved by the Administrator or Authorized Departmental Officers (ADOs) upon determination that the project will contribute toward accomplishment of the Agency's overall mission and meet any established project evaluation/selection criteria.",
        "deadlines": {"flag": "contact", "list": []},
        "approval_time": "From 60 to 120 days.",
        "appeals": "None",
        "renewals": "Based on program needs and availability of annual funding.",
        "requirements": {
            "types": {"moe": False, "formula": False, "matching": False},
            "formula": {
                "title": "",
                "chapter": "",
                "part": "",
                "subPart": "",
                "publicLaw": "",
                "description": "",
            },
            "matching": {"description": ""},
            "moe": {"description": ""},
        },
        "assistance_period": {
            "awarded": "other",
            "description": "Up to 1 year from the date of award.  Funds are made available as required to cover expenditures.",
            "awardedDescription": "Funds are provided to recipients when requests for advance or reimbursement are received and approved by the Agency.",
        },
        "reports": [
            {"code": "program", "isSelected": False, "description": ""},
            {"code": "cash", "isSelected": False, "description": ""},
            {
                "code": "progress",
                "isSelected": True,
                "description": "Requirements are specifically indicated in the award documents and may vary for given programs; however, quarterly financial reports, annual progress reports, final financial and final summary progress reports are generally required.",
            },
            {
                "code": "expenditure",
                "isSelected": True,
                "description": "SF-425, Federal Financial Report",
            },
            {
                "code": "performanceMonitoring",
                "isSelected": True,
                "description": "Narrative performance progress reports",
            },
        ],
        "audits": {"isApplicable": True, "description": "N/A"},
        "records": "Instruction provided in the Notice of Award.  Grantees are expected to maintain separate records for each grant to ensure that funds are used for the purpose for which the grant was made.  Records are subject to inspection during the life of the grant and for three years thereafter.",
        "account_identification": "12-9971-0-7-352;12-1600-0-1-352;",
        "obligations": "(Salaries and Expenses) FY 18$246,769,118.00; FY 19 est $249,527,131.00; FY 20 est $280,732,387.00; FY 17$243,631,584.00; FY 16$239,406,515.00; - APHIS has a difference between budget authority and obligations because there is carryover funding available from no year funding.\n",
        "assistance_range": "",
        "program_accomplishments": {
            "list": [
                {
                    "fiscalYear": 2016,
                    "description": "Selected examples of progress: Brucellosis class free status States - 50 States and 3 Territories; \r\nTuberculosis - number of States/Territories recognized as TB free - 48 States, 2 Territories Selected examples of progress: Brucellosis class free status States - 50 States and 3 Territories; \r\nTuberculosis - number of States/Territories recognized as TB free - 49 States, 2 Territories ",
                },
                {
                    "fiscalYear": 2017,
                    "description": "Selected examples of progress: Brucellosis class free status States - 50 States and 3 Territories; \r\nTuberculosis - number of States/Territories recognized as TB free - 49 States, 2 Territories",
                },
                {
                    "fiscalYear": 2018,
                    "description": "Selected examples of progress: Brucellosis class free status States - 50 States and 3 Territories; \r\nTuberculosis - number of States/Territories recognized as TB free - 49 States, 2 Territories",
                },
                {
                    "fiscalYear": 2019,
                    "description": "Selected examples of progress: Brucellosis class free status States - 50 States and 3 Territories; Tuberculosis - number of States/Territories recognized as TB free - 49 States, 2 Territories",
                },
                {
                    "fiscalYear": 2020,
                    "description": "Selected examples of progress: Brucellosis class free status States - 50 States and 3 Territories; Tuberculosis - number of States/Territories recognized as TB free - 49 States, 2 Territories",
                },
            ],
            "isApplicable": True,
        },
        "regulations": 'Uniform Administrative Requirements, Cost Principles, and Audit Requirements for Federal Awards<94>, 2 CFR Part 200; Nonprocurement  Debarment and Suspension<94> 2 CFR 417; <93>Requirements for Drug-Free Workplace", 2 CFR Part 421; "New Restrictions on Lobbying", 2 CFR Part 418; and Office of Management and Budget regulations governing "Controlling Paperwork Burdens on the Public", 5 CFR 1320',
        "regional_local_office": {
            "flag": "appendix",
            "description": "Consult Appendix IV of the Catalog for addresses of regional offices of the Animal and Plant Health Inspection Service.",
        },
        "headquarters_office": "Eileen M. Berke,4700 River Road, Unit 55, Riverdale, MD 20737 Email:< a href='mailto:eileen.m.berke@aphis.usda.gov'>eileen.m.berke@aphis.usda.gov</a>Phone: (301) 851-2856;",
        "website": "http://www.aphis.usda.gov/",
        "related_programs": "10.207 Animal Health and Disease Research; 10.215 Sustainable Agriculture Research and Education; 10.219 Biotechnology Risk Assessment Research; 15.611 Wildlife Restoration and Basic Hunter Education; 10.001 Agricultural Research Basic and Applied Research; 10.500 Cooperative Extension Service; 10.028 Wildlife Services; 10.202 Cooperative Forestry Research; 10.902 Soil and Water Conservation; 10.250 Agricultural and Rural Economic Research, Cooperative Agreements and Collaborations; 10.652 Forestry Research; ",
        "funded_project_examples": "Not Applicable.",
        "selection_criteria": "Not Applicable.",
        "published_date": datetime.date(1972, 1, 1),
        "parent_shortname": "USDA",
        "sam_gov_url": "https://beta.sam.gov/fal/b3ecfc858fc946748a843a8fa561f817/view",
        "recovery": False,
    },
    {
        "program_title": "Wildlife Services",
        "program_number": "10.028",
        "popular_name": "",
        "federal_agency": "ANIMAL AND PLANT HEALTH INSPECTION SERVICE, AGRICULTURE, DEPARTMENT OF",
        "authorization": {
            "list": [
                {
                    "act": {"description": "Animal Damage Control Act of 1931"},
                    "USC": {"title": "7", "section": "426,426b, 426c"},
                    "authorizationTypes": {"USC": True, "act": True},
                    "usc": {"title": "7", "section": "426,426b, 426c"},
                },
                {
                    "publicLaw": {"congressCode": "115", "number": "334"},
                    "USC": {"title": "7 USC"},
                    "authorizationTypes": {"publicLaw": True},
                    "usc": {"title": "7 USC"},
                },
            ]
        },
        "objectives": "To reduce damage caused by mammals and birds and those mammal and bird species that are reservoirs for zoonotic diseases, (except for urban rodent control through control and research activities).  Wherever feasible, humane methods will be emphasized.",
        "assistance_types": "PROJECT GRANTS",
        "uses_restrictions": "Not Applicable",
        "applicant_eligibility": "State and local governments, federally recognized Indian tribal governments, public/private nonprofit organizations, nonprofit institutions of higher education, and individuals.",
        "beneficiary_eligibility": "States, local jurisdictions, U.S. Territorial government agencies, federally recognized Indian tribal governments, public and private institutions and organizations, farmers, ranchers, agricultural producers, and land/property owners benefit from Federal assistance in the control of nuisance mammals and birds and those mammal and bird species that are reservoirs for zoonotic diseases.",
        "credentials_documentation": {
            "description": "Curriculum vitae for principal investigator, except for State, local, and Territorial government cooperators.",
            "isApplicable": True,
        },
        "preapplication_coordination": {
            "environmentalImpact": {
                "reports": [
                    {"isSelected": True, "reportCode": "ExecutiveOrder12372"},
                    {"isSelected": True, "reportCode": "otherRequired"},
                ]
            },
            "description": "N/A",
        },
        "application_procedures": {},
        "award_procedure": "Applications are approved by the Administrator or authorized departmental officers (ADO's) upon determination that the project will contribute toward accomplishment of the Agency's overall mission and meet any established project evaluation/selection criteria.",
        "deadlines": {"flag": "no", "list": []},
        "approval_time": "From 60 to 120 days.",
        "appeals": "Not Applicable",
        "renewals": "Based on program needs and availability of annual funding.",
        "requirements": {
            "types": {"moe": False, "formula": False, "matching": False},
            "formula": {
                "title": "",
                "chapter": "",
                "part": "",
                "subPart": "",
                "publicLaw": "",
                "description": "",
            },
            "matching": {"description": ""},
            "moe": {"description": ""},
        },
        "assistance_period": {
            "awarded": "other",
            "description": "Up to one year from the date of award.  Funds are made available as required to cover expenditures.",
            "awardedDescription": "Funds are provided to recipients when requests for advance or reimbursement are received and approved by the Agency.",
        },
        "reports": [
            {"code": "program", "isSelected": False, "description": ""},
            {"code": "cash", "isSelected": False, "description": ""},
            {"code": "progress", "isSelected": False, "description": ""},
            {
                "code": "expenditure",
                "isSelected": True,
                "description": "SF-425, Federal Financial Report",
            },
            {
                "code": "performanceMonitoring",
                "isSelected": True,
                "description": "Requirements are specifically indicated in the award documents and may vary for given programs.  Narrative performance progress reports.",
            },
        ],
        "audits": {"isApplicable": True, "description": "N/A"},
        "records": "Instruction provided in the Notice of Award.  Grantees are expected to maintain separate records for each grant to ensure that funds are used for the purpose for which the grant was made.  Records are subject to inspection during the life of the grant and for three years thereafter.",
        "account_identification": "12-1600-0-1-352;",
        "obligations": "(Salaries and Expenses) FY 18$7,905,018.00; FY 19 est $8,063,118.00; FY 20 est $13,466,274.00; FY 17$8,583,390.00; FY 16$6,649,664.00; - APHIS has a difference between budget authority and obligations because there is carryover funding available from no year funding.",
        "assistance_range": "No Data Available. ",
        "program_accomplishments": {"list": [], "isApplicable": False},
        "regulations": 'Uniform Administrative Requirements, Cost Principles, and Audit Requirements for Federal Awards<94>, 2 CFR Part 200; Nonprocurement  Debarment and Suspension<94> 2 CFR 417; <93>Requirements for Drug-Free Workplace", 2 CFR Part 421; "New Restrictions on Lobbying", 2 CFR Part 418; and Office of Management and Budget regulations governing "Controlling Paperwork Burdens on the Public", 5 CFR 1320',
        "regional_local_office": {
            "flag": "appendix",
            "description": "See Appendix IV of the Catalog.",
        },
        "headquarters_office": "Eileen M. Berke,4700 River Road, Unit 55, Suite 3B06.3, Riverdale, MD 20737 Email:< a href='mailto:eileen.m.berke@aphis.usda.gov'>eileen.m.berke@aphis.usda.gov</a>Phone: (301) 851-2856;",
        "website": "http://www.aphis.usda.gov",
        "related_programs": "15.611 Wildlife Restoration and Basic Hunter Education; 10.025 Plant and Animal Disease, Pest Control, and Animal Care; 10.652 Forestry Research; ",
        "funded_project_examples": "Not Applicable.",
        "selection_criteria": "Relevance to agency program mission and qualification of principle investigator and institution.",
        "published_date": datetime.date(1986, 1, 1),
        "parent_shortname": "USDA",
        "sam_gov_url": "https://beta.sam.gov/fal/64380a8c942f4c8b82e84baf7eec21f7/view",
        "recovery": False,
    },
    {
        "program_title": "Indemnity Program",
        "program_number": "10.030",
        "popular_name": "",
        "federal_agency": "ANIMAL AND PLANT HEALTH INSPECTION SERVICE, AGRICULTURE, DEPARTMENT OF",
        "authorization": {
            "list": [
                {
                    "act": {"description": "Plant Protection Act"},
                    "publicLaw": {"number": "106-224"},
                    "authorizationTypes": {"act": True, "publicLaw": True},
                },
                {
                    "act": {"description": "9 CFR parts 50-54"},
                    "authorizationTypes": {"act": True},
                },
            ]
        },
        "objectives": "Animal and Plant Health Inspection Service administers regulations at 9 CFR parts 50 to 54 that authorizes payment for indemnities.  This authority covers a wide variety of indemnity situations ranging from large livestock depopulations to small fowl depopulations, and there are various indemnity calculations and processes for determining the indemnity value for each specific species.  The Secretary of Agriculture offers an opinion that constitutes an emergency and threatens the U.S. animal population.  Payment for the destroyed animals is based on fair market value.  Also, under Section 415 (e) of the Plant Protection Act (Title IV of Public Law 106-224), under a declaration of extraordinary emergency because of the presence of a plant pest or noxious weed that is new to or not known to be widely prevalent in the United States, the Secretary may pay compensation for economic losses incurred by as a result of actions taken under the authorities in this section (415).\n",
        "assistance_types": "DIRECT PAYMENTS WITH UNRESTRICTED USE",
        "uses_restrictions": "Not Applicable",
        "applicant_eligibility": "N/A",
        "beneficiary_eligibility": "N/A",
        "credentials_documentation": {
            "description": "Required documentation will be specified in the Declaration of Emergency issued by the Secretary of Agriculture",
            "isApplicable": True,
        },
        "preapplication_coordination": {},
        "application_procedures": {"description": "N/A"},
        "award_procedure": "Required documentation will be specified in the Declaration of Emergency issued by the Secretary of Agriculture",
        "deadlines": {"flag": "no", "list": []},
        "approval_time": "Not Applicable",
        "appeals": "Not Applicable",
        "renewals": "Not Applicable",
        "requirements": {"types": {"moe": False, "formula": False, "matching": False}},
        "assistance_period": {
            "awarded": "other",
            "description": "Time period of availability will be specified in the Declaration of Emergency issued by the Secretary of Agriculture",
            "awardedDescription": "Electronic Funds Transfer or paper check",
        },
        "reports": [
            {"code": "program", "isSelected": False},
            {"code": "cash", "isSelected": False},
            {"code": "progress", "isSelected": False},
            {"code": "expenditure", "isSelected": False},
            {"code": "performanceMonitoring", "isSelected": False},
        ],
        "audits": {"isApplicable": False},
        "records": "Record requirements will be specified in the Declaration of Emergency issued by the Secretary of Agriculture",
        "account_identification": "12-1600-0-1-352;",
        "obligations": "(Direct Payments with Unrestricted Use) FY 18$6,586,698.00; FY 19 est $13,751,903.00; FY 20 est $14,400,228.00; FY 17$6,794,055.00; FY 16$30,472,730.00; - ",
        "assistance_range": "No Data Available. ",
        "program_accomplishments": {"list": [], "isApplicable": False},
        "regulations": "Not Applicable.",
        "regional_local_office": {"flag": "appendix"},
        "headquarters_office": "Donna Cichy100 North 6th Street, Suite 510C\n, Minneapolis, MN 55403 Email:< a href='mailto:Donna.R.Cichy@aphis.usda.gov'>Donna.R.Cichy@aphis.usda.gov</a>Phone: 6123363261;",
        "website": "Not Applicable",
        "related_programs": "Not Applicable.",
        "funded_project_examples": "Not Applicable.",
        "selection_criteria": "Not Applicable.",
        "published_date": datetime.date(2012, 3, 16),
        "parent_shortname": "USDA",
        "sam_gov_url": "https://beta.sam.gov/fal/ea43970d0f5949fea2d0e7b1597c10ff/view",
        "recovery": False,
    },
    {
        "program_title": "Commodity Loans and Loan Deficiency Payments",
        "program_number": "10.051",
        "popular_name": "Marketing Assistance Loans (MAL's) and Loan Deficiency Payments (LDP's)",
        "federal_agency": "FARM SERVICE AGENCY, AGRICULTURE, DEPARTMENT OF",
        "authorization": {
            "list": [
                {
                    "act": {"description": "Agricultural Act of 2014"},
                    "publicLaw": {"congressCode": "113", "number": "79"},
                    "authorizationTypes": {"act": True, "publicLaw": True},
                },
                {
                    "act": {},
                    "parentAuthorizationId": "49a6782a35c341e758eb9435a2cb56bd",
                    "publicLaw": {"congressCode": "115", "number": "334"},
                    "authorizationTypes": {"act": True, "publicLaw": True},
                },
            ]
        },
        "objectives": "To improve and stabilize farm income, to assist in bringing about a better balance between supply and demand of the commodities, and to assist farmers in the orderly marketing of their crops.",
        "assistance_types": "DIRECT PAYMENTS WITH UNRESTRICTED USE;DIRECT LOANS",
        "uses_restrictions": "Not Applicable",
        "applicant_eligibility": "Owner, landlord, tenant, or sharecropper on an eligible farm that has produced the eligible commodities or, in the case of sugar, a processor or refiner who meets program requirements as announced by the Secretary.",
        "beneficiary_eligibility": "Owner, landlord, tenant, or sharecropper on a farm that has produced the eligible commodities, meets program requirements as announced by the Secretary, and maintains beneficial interest in the commodity.  State and County governments may be eligible for MAL's and LDP's when they have a share in produced and harvested eligible commodities on land they own, if the benefits or payments are used to support public schools.",
        "credentials_documentation": {
            "description": "The commodity must be produced and harvested by the producer, and the producer must meet program requirements as announced by the Secretary.  Requirements include a record of the farming operation on file in the FSA county office and a complete acreage report to account for all cropland on the farm must be submitted for the applicable crop year.  ",
            "isApplicable": True,
        },
        "preapplication_coordination": {
            "environmentalImpact": {
                "reports": [{"isSelected": True, "reportCode": "otherRequired"}]
            },
            "description": "No additional information provided.",
        },
        "application_procedures": {
            "description": "In the case of warehouse-stored commodities, producer or Cooperative Marketing Association presents warehouse receipts to the FSA county office (warehouse-stored peanut loans may be made through Designated Marketing Associations).  In the case of farm-stored commodities (including sugar), producer/processor or Cooperative Marketing Association requests a loan at the FSA county office."
        },
        "award_procedure": "Applications are approved by the FSA upon determination that applicant and commodity are eligible.",
        "deadlines": {
            "flag": "yes",
            "description": "Deadline for the year following year in which crop is normally harvested is as follows:January 31st - MAL's and LDP's are available for peanuts and wool.     March 31st - MAL's and LDP's are available for wheat, barley, oats, canola, flaxseed, crambe, rapeseed, sesame seed, and honey; May 31st - MAL's and LDP's are available for rice, corn, grain sorghum, cotton, soybeans, safflower, sunflower seed, mustard seed, small and large chickpeas, lentils, dry peas , and cotton; and September 30th - Loans are available for sugar.",
            "list": [],
        },
        "approval_time": "Approximately 3 days but could take from 15 to 30 days.",
        "appeals": "Applications may be reviewed by county, State, or national offices.",
        "renewals": "Not Applicable",
        "requirements": {
            "types": {"moe": False, "formula": False, "matching": False},
            "formula": {
                "title": "",
                "chapter": "",
                "part": "",
                "subPart": "",
                "publicLaw": "",
                "description": "",
            },
            "matching": {"description": ""},
            "moe": {"description": ""},
        },
        "assistance_period": {
            "awarded": "lump",
            "description": "Assistance is generally available for 9 months or less, and is normally disbursed on a lump-sum basis.",
        },
        "reports": [
            {"code": "program", "isSelected": False, "description": ""},
            {"code": "cash", "isSelected": False, "description": ""},
            {"code": "progress", "isSelected": False, "description": ""},
            {"code": "expenditure", "isSelected": False, "description": ""},
            {"code": "performanceMonitoring", "isSelected": False, "description": ""},
        ],
        "audits": {
            "isApplicable": True,
            "description": "Periodic and required spot checks of farm-stored grain will be made by the county FSA office.  Recipients are subject to other audits by FSA and by the Office of Inspector General, USDA.",
        },
        "records": "Not applicable.",
        "account_identification": "12-4336-0-3-999;",
        "obligations": "(Direct Loans) FY 18$3,145,610,000.00; FY 19 est $3,205,858,000.00; FY 20 est $3,159,314,000.00; FY 17$6,914,144,153.00; FY 16$6,560,230,313.00; - (Direct Payments with Unrestricted Use) FY 18$72,000.00; FY 19 est $33,451,000.00; FY 20 est $65,467,000.00; FY 17$46,564,581.00; FY 16$212,967,255.00; - Loan Deficiency Payments",
        "assistance_range": "",
        "program_accomplishments": {"list": [], "isApplicable": False},
        "regulations": 'Program regulations published in the Federal Register 7 CFR, Chapter XIV, Parts 1421, 1425, 1427, 1434, and 1435; announcements issued to news media and letters to producers; " FSA Commodity Fact Sheets, " no cost: The Price Support Program," ; Farm Service Agency, Department of Agriculture, STOP 0506, 1400 Independence Avenue S.W., Washington, DC 20250-0506.',
        "regional_local_office": {
            "flag": "appendix",
            "description": "Consult the appropriate FSA State office where the property is located. For a list of FSA State offices with telephone numbers and addresses, information is available on the internet, visit FSA website at www.fsa.usda.gov to locate nearest office.",
        },
        "headquarters_office": "Shayla Watson-Porter1400 Independence Avenue, SW, Stop 0510, Washington, DC 20250-0510 Email:< a href='mailto:Shayla.watson-porter@usda.gov'>Shayla.watson-porter@usda.gov</a>Phone: (202) 690-2350;",
        "website": "http://www.fsa.usda.gov/programs-and-services/price-support/Index",
        "related_programs": "10.155 Marketing Agreements and Orders; ",
        "funded_project_examples": "Not Applicable.",
        "selection_criteria": "Not Applicable.",
        "published_date": datetime.date(1965, 1, 1),
        "parent_shortname": "USDA",
        "sam_gov_url": "https://beta.sam.gov/fal/d61fdbf7a47245ce807c41dea841f1f1/view",
        "recovery": False,
    },
    {
        "program_title": "Dairy Indemnity Program",
        "program_number": "10.053",
        "popular_name": "DIPP",
        "federal_agency": "FARM SERVICE AGENCY, AGRICULTURE, DEPARTMENT OF",
        "authorization": {
            "list": [
                {
                    "act": {"description": "Act of August 13, 1968"},
                    "publicLaw": {"number": "90-484"},
                    "statute": {"page": "750", "volume": "82"},
                    "USC": {"title": "7", "section": "450j-450l"},
                    "authorizationTypes": {
                        "USC": True,
                        "act": True,
                        "statute": True,
                        "publicLaw": True,
                    },
                    "usc": {"title": "7", "section": "450j-450l"},
                },
                {
                    "act": {},
                    "publicLaw": {"congressCode": "115", "number": "334"},
                    "authorizationTypes": {"act": True, "publicLaw": True},
                },
            ]
        },
        "objectives": "To protect dairy farmers and manufacturers of dairy products who through no fault of their own, are directed to remove their milk or dairy products from commercial markets because of contamination from pesticides which have been approved for use by the Federal government.  Dairy farmers can also be indemnified because of contamination with chemicals or toxic substances, nuclear radiation or fallout.",
        "assistance_types": "DIRECT PAYMENTS WITH UNRESTRICTED USE",
        "uses_restrictions": "Not Applicable",
        "applicant_eligibility": "Dairy farmers whose milk has been removed from the market by a public agency because of residue of any violating substance in such milk.  Manufacturers of dairy products whose product has been removed from the market by a public agency because of pesticide residue in such product.  This program is also available in Puerto Rico.",
        "beneficiary_eligibility": "Dairy farmers whose milk has been removed from the market by a public agency because of residue of any violating substance in such milk. Manufacturers of dairy products whose product has been removed from the market by a public agency because of pesticide residue in such product. This program is available in Puerto Rico.",
        "credentials_documentation": {
            "description": "In the case of a dairy farmer, the notice removing the milk from the market along with a record of past marketing records for milk to determine the quantity and value of the milk not marketed, the violating substance involved and the uses of such violating substances during the previous 24 months.  In the case of the manufacturer of dairy products, the notice removing the product from the market and sufficient data to determine the value of the product.  This program is excluded from coverage under OMB Circular No. A-87.",
            "isApplicable": True,
        },
        "preapplication_coordination": {"environmentalImpact": {"reports": []}},
        "application_procedures": {
            "description": "Producers must file an application for payment on Form FSA-373 with the local county FSA office. Manufacturers must file information on the cause and amount of their loss with the local county FSA office.  "
        },
        "award_procedure": "Initial approval is made by the county FSA committee.  Final approval is made by the Price Support Division in Washington, DC.",
        "deadlines": {
            "flag": "yes",
            "description": "Claims must be filed by December 31 following the fiscal year in which the loss has occurred.",
            "list": [{"start": "2019-01-01", "end": "2023-12-31"}],
        },
        "approval_time": "From 60 to 90 days.",
        "appeals": "Applicants may appeal to the county Farm Service Agency Committee and to the FSA, Department of Agriculture,  Appeals and Litigation Group, 1400 Independence Avenue, SW., Washington, DC 20250-0570.",
        "renewals": "Not Applicable",
        "requirements": {
            "types": {"moe": False, "formula": False, "matching": False},
            "formula": {
                "title": "",
                "chapter": "",
                "part": "",
                "subPart": "",
                "publicLaw": "",
                "description": "",
            },
            "matching": {"description": ""},
            "moe": {"description": ""},
        },
        "assistance_period": {
            "awarded": "lump",
            "description": "Payment is made by Commodity Credit Corporation (CCC) check after claim approval.",
        },
        "reports": [
            {"code": "program", "isSelected": False, "description": ""},
            {"code": "cash", "isSelected": False, "description": ""},
            {"code": "progress", "isSelected": False, "description": ""},
            {"code": "expenditure", "isSelected": False, "description": ""},
            {"code": "performanceMonitoring", "isSelected": False, "description": ""},
        ],
        "audits": {"isApplicable": False, "description": ""},
        "records": "The dairy farmer and the manufacturer of dairy products must keep any records in applying for a payment for 3 years following the year in which an application for payment was filed.",
        "account_identification": "12-1140-0-1-351;",
        "obligations": "(Direct Payments with Unrestricted Use) FY 18$173,000.00; FY 19 est $3,439,646.00; FY 20 est $500,000.00; FY 17$224,334.00; FY 16$161,410.00; - ",
        "assistance_range": "No Payment Limitation.",
        "program_accomplishments": {"list": [], "isApplicable": False},
        "regulations": "Program regulations were published in the Federal Register, 7 CFR, 760, and announced through the news media, Handbook 3-LD, Circulars and regulations issued by FSA.",
        "regional_local_office": {
            "flag": "appendix",
            "description": "Consult the appropriate FSA State office where the property is located. For a list of FSA State offices with telephone numbers and addresses, information is available on the internet, visit FSA website at www.fsa.usda.gov to locate nearest office.",
        },
        "headquarters_office": "Douglas E. Kilgore1400 Independence Avenue, SW, Washington, DC 20250-0512 Email:< a href='mailto:Douglas.E.Kilgore@usda.gov'>Douglas.E.Kilgore@usda.gov</a>Phone: (202) 720-9011;",
        "website": "http://www.fsa.usda.gov/programs-and-services/price-support/Index",
        "related_programs": "10.500 Cooperative Extension Service; ",
        "funded_project_examples": "Not Applicable.",
        "selection_criteria": "Not Applicable.",
        "published_date": datetime.date(1969, 1, 1),
        "parent_shortname": "USDA",
        "sam_gov_url": "https://beta.sam.gov/fal/53b8e30429bd42b8b443712d9f307953/view",
        "recovery": False,
    },
]
