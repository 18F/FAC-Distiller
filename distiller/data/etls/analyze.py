import json
import sys

from . import nlp
from . import heuristics
from . import pdf_utils


def analyze(processor, pdf):
    """
    For every page in the PDF, analyze the text and see if we can
    extract either a finding or a corrective action plan from it. In
    either case, an audit number is required.
    """
    results = []
    pages = pdf_utils.all_pages(pdf)
    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]
        sys.stdout.write(f'Processing page {page_number}.\n')
        sys.stdout.flush()
        page_doc = processor(page_text)
        audits = nlp.get_audit_numbers(page_doc)
        for audit in audits:
            hit = analyze_doc(page_doc, audit, page_number)
            if hit:
                hit["page_number"] = page_number # stash for future reference
                results.append(hit)
    # clean up the results if applicable
    # TODO not working
    return heuristics.apply_all_heuristics(results)


def analyze_doc(page_doc, audit, page_number):
    """
    Given a page document and an audit reference, extract as much
    information about the referenced audit as possible. This function
    may return None if no keywords are found in proximity to the audit
    reference.
    """
    finding = nlp.extract_finding(page_doc, audit)
    # TODO match against audit
    cap = nlp.extract_cap(page_doc)
    if finding or cap:
        # if we have a finding, supplement with secondary keywords and page number
        finding_dict = dict()
        if finding:
            finding_dict['Finding'] = finding
            finding_dict['Page number'] = page_number
            secondaries = nlp.get_secondaries(page_doc)
            finding_dict.update(secondaries)
        # if we have a cap, only add the page number
        cap_dict = dict()
        if cap:
            cap_dict['Plan'] = cap
            cap_dict['Page number'] = page_number
        return dict(
            audit=audit,
            finding_text=json.dumps(finding_dict),
            cap_text=json.dumps(cap_dict),
        )
    return None
