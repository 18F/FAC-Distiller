import sys

from . import nlp
from . import heuristics
from . import pdf_utils


def analyze(processor, pdf, silent=False):
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
        if not silent:
            sys.stdout.write(f"Processing page {page_number}.\n")
            sys.stdout.flush()
        page_doc = processor(page_text)
        audits = nlp.get_audit_numbers(page_doc)
        for audit in audits:
            hit = analyze_doc(page_doc, audit, page_number)
            if hit:
                results.append(hit)
    return results


def analyze_doc(page_doc, audit, page_number):
    """
    Given a page document and an audit reference, extract as much
    information about the referenced audit as possible. This function
    may return None if no keywords are found in proximity to the audit
    reference.
    """
    finding = nlp.extract_finding(page_doc, audit)
    cap = nlp.extract_cap(page_doc, audit)
    if finding or cap:
        # if we have a finding, supplement with secondary keywords and page number
        finding_dict = dict()
        if finding:
            finding_dict["Finding"] = finding
            finding_dict["Page number"] = page_number
            secondaries = nlp.get_secondaries(page_doc)
            finding_dict.update(secondaries)
            # clean up the results if applicable
            finding_dict = heuristics.apply_all_heuristics(finding_dict)
            if not finding_dict:
                return None
        # if we have a cap, only add the page number
        cap_dict = dict()
        if cap:
            cap_dict["Plan"] = cap
            cap_dict["Page number"] = page_number
        return dict(
            audit=audit,
            finding_data=finding_dict,
            cap_data=cap_dict,
            page_number=page_number,
        )
    return None


def output_as_csv(results):
    """
    Output analyzed results in a format suitable for CSV. Audit
    number, finding, CAP, and page number columns are always present.
    Additional finding keywords, if any, are added as extra columns.
    """
    from functools import reduce

    base_header = [
        "audit number",
        "finding data",
        "corrective action plan",
        "page number",
    ]
    headers = reduce(
        lambda accum, x: accum | set(x["finding_data"].keys()), results, set()
    )
    headers.discard("Finding")  # may be already present in base header
    headers.discard("Page number")  # may be already present in base header
    yield base_header + list(headers)

    for result in results:
        audit = result["audit"]
        page_number = result["page_number"]
        finding = result["finding_data"].get("Finding", "")
        cap = result["cap_data"].get("Plan", "")
        rest = map(lambda h: result["finding_data"].get(h, ""), headers)
        yield [audit, finding, cap, page_number] + list(rest)


if __name__ == "__main__":
    import argparse
    import csv
    import pickle

    from distiller.gateways import files

    parser = argparse.ArgumentParser(
        description="Extract audit data from the given PDF."
    )
    parser.add_argument("filename")
    parser.add_argument("--csv", help="store output to a CSV file")
    parser.add_argument("--pickle", help="store output to a pickle file")
    parser.add_argument("--errors", help="record errors", action="store_true")
    args = parser.parse_args()

    pdf = files.input_file(args.filename, mode="rb")
    pdf_errors = pdf_utils.errors(pdf)

    if pdf_errors and args.errors:
        if args.pickle:
            with files.output_file(args.pickle, mode="wb") as fd:
                pickle.dump(pdf_errors, fd)
        elif args.csv:
            with files.output_file(args.csv, mode="w") as fd:
                cw = csv.writer(fd)
                cw.writerow(["error"])
                for line in pdf_errors:
                    cw.writerow([line])
        else:
            for error in errors:
                print(error)
        sys.exit(1)

    if pdf_errors:
        print(f"Could not read file {args.filename}: {pdf_errors}. Bailing out.")
        sys.exit(1)

    print(f"processing {args.filename}")
    processor = nlp.setup()
    audit_results = analyze(processor, pdf, silent=True)

    if not audit_results:
        print(f"processed {args.filename} with no results")
        sys.exit(1)

    if args.pickle:
        with files.output_file(args.pickle, mode="wb") as fd:
            pickle.dump(audit_results, fd)
    elif args.csv:
        with files.output_file(args.csv, mode="w") as fd:
            cw = csv.writer(fd)
            for line in output_as_csv(audit_results):
                cw.writerow(line)
    else:
        for result in audit_results:
            print(result)

    print(f"processed {args.filename} with {len(audit_results)} results")
