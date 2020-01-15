"""
Audit search form and related code.

@todo soon enough: Separate this into its own tiny extension/module so you can
import it both here and in the file that's actually doing the filtering.
"""

from collections import defaultdict

from django import forms

from distiller.data.models import AssistanceListing


# This is a dictionary of agencies indexed by their two-digit Federal Agency
# Prefixes, as specified on the Federal Audit Clearinghouse.
#
# The prefixes must be strings. Otherwise we'll lose the leading zeroes.
# Since Python 3.6, dictionaries are OrderedDicts by default, so we don't need
# to do anything special to keep the agency names in alphabetical order.
#
# Since agencies may share a prefix, don't store this as a dictionary.
#
AGENCY_CHOICES = (
    ('01', 'African Development Foundation'),
    ('23', 'Appalachian Regional Commission'),
    ('88', 'Architectural & Transporation Barriers Compliance Board'),
    ('13', 'Central Intelligence Agency'),
    ('29', 'Commission on Civil Rights'),
    ('78', 'Commodity Futures Trading Commission'),
    ('87', 'Consumer Product Safety Commission'),
    ('94', 'Corporation for National and Community Service'),
    ('90', 'Delta Regional Authority'),
    ('90', 'Denali Commission'),
    ('10', 'Department of Agriculture'),
    ('11', 'Department of Commerce'),
    ('12', 'Department of Defense'),
    ('84', 'Department of Education'),
    ('81', 'Department of Energy'),
    ('93', 'Department of Health and Human Services'),
    ('97', 'Department of Homeland Security'),
    ('14', 'Department of Housing and Urban Development'),
    ('15', 'Department of the Interior'),
    ('16', 'Department of Justice'),
    ('17', 'Department of Labor'),
    ('19', 'Department of State'),
    ('20', 'Department of Transportation'),
    ('21', 'Department of Treasury'),
    ('64', 'Department of Veterans Affairs'),
    ('90', 'Election Assistance Commission'),
    ('66', 'Environmental Protection Agency'),
    ('30', 'Equal Employment Opportunity Commission'),
    ('95', 'Executive Office of the President'),
    ('32', 'Federal Communications Commission'),
    ('83', 'Federal Emergency Management Agency'),
    ('33', 'Federal Maritime Commission'),
    ('34', 'Federal Mediation and Conciliation Service'),
    ('18', 'Federal Reserve System'),
    ('36', 'Federal Trade Commission'),
    ('39', 'General Services Administration'),
    ('40', 'Government Printing Office'),
    ('03', 'Institute of Museum and Library Services'),
    ('04', 'Inter-American Foundation'),
    ('61', 'International Trade Commission'),
    ('90', 'Japan U.S. Friendship Commission'),
    ('09', 'Legal Services Corporation'),
    ('42', 'Library of Congress'),
    ('43', 'National Aeronautics & Space Administration'),
    ('89', 'National Archives & Records Administration'),
    ('92', 'National Council on Disability'),
    ('44', 'National Credit Union Administration'),
    ('05', 'National Endowment for the Arts'),
    ('06', 'National Endowment for the Humanities'),
    ('45', 'National Foundation on the Arts and the Humanities'),
    ('68', 'National Gallery of Art'),
    ('46', 'National Labor Relations Board'),
    ('47', 'National Science Foundation'),
    ('77', 'Nuclear Regulatory Commission'),
    ('07', 'Office of National Drug Control Policy'),
    ('27', 'Office of Personnel Management'),
    ('70', 'Overseas Private Investment Corporation'),
    ('08', 'Peace Corps'),
    ('86', 'Pension Benefit Guaranty Corporation'),
    ('22', 'Postal Service'),
    ('53', "President's Committee on Employment of People with Disabilities"),
    ('57', 'Railroad Retirement Board'),
    ('85', 'Scholarship Foundations'),
    ('58', 'Securities and Exchange Commission'),
    ('59', 'Small Business Administration'),
    ('60', 'Smithsonian Institution'),
    ('96', 'Social Security Administration'),
    ('62', 'Tennessee Valley Authority'),
    ('98', 'U.S. Agency for International Development'),
    ('82', 'United States Information Agency'),
    ('91', 'United States Institute of Peace'),
    ('99', 'Miscellaneous'),
)

AGENCIES_BY_PREFIX = defaultdict(list)
for choice in AGENCY_CHOICES:
    AGENCIES_BY_PREFIX[choice[0]].append(choice[1])


class AgencySelectionForm(forms.Form):
    agency = forms.ChoiceField(choices=AGENCY_CHOICES)
    sub_agency = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Support filtering on subagency, default to first choice
        agency = self['agency'].value()
        self.fields['sub_agency'].choices = [
            (agency, 'All sub-agencies')
        ] + [
            sub_agency
            for sub_agency in AssistanceListing.objects.subagencies_for_prefix(
                agency).values_list('program_number', 'program_title')
        ]
