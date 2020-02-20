from spacy.pipeline import EntityRuler
import spacy

import re


def clean(s):
    """
    Attempt to render the (possibly extracted) string as legible as possible.
    """
    result = s.strip().replace("\n", " ")
    result = result.replace("\u00a0", " ")  # no-break space
    result = result.replace("\u000c", " ")  # vertical tab
    while "  " in result:
        result = result.replace("  ", " ")
    return result


def startswith(s, prefix):
    return s[s.find[prefix] :]


def split_pattern(string):
    return [{"LOWER": s} for s in string.split(" ")]


# a sample of different headers that start audit findings
headers = [
    "findings and questioned costs",
    "status of prior year findings",
    "questioned costs for federal awards",
    "federal award findings and questioned costs",
    "financial statement findings",
    "major federal award programs audit",
    "findings – financial statement audit",
    "findings related to the financial statements"
    "major federal award findings and questioned costs",
    "summary schedule of prior audit findings",
]

# phrases that may indicate CAP text
corrective_actions = [
    "corrective action",
    "corrective action plan",
    "planned corrective actions",
    "planned corrective action",
]

patterns = [
    # secondary criteria: used to identify where the audit is
    {"label": "CONDITION", "pattern": [{"LOWER": "observation"}]},
    {"label": "CONDITION", "pattern": [{"LOWER": "condition"}]},
    {"label": "CRITERIA", "pattern": [{"LOWER": "criteria"}]},
    {"label": "CRITERIA", "pattern": split_pattern("criteria or specific requirement")},
    {"label": "CONTEXT", "pattern": [{"LOWER": "context"}]},
    {"label": "CAUSE", "pattern": [{"LOWER": "cause"}]},
    {"label": "CAUSE", "pattern": split_pattern("cause of the condition")},
    {"label": "EFFECT", "pattern": [{"LOWER": "effect"}]},
    {"label": "EFFECT", "pattern": split_pattern("effect or possible effect")},
    {"label": "RECOMMENDATION", "pattern": [{"LOWER": {"REGEX": "recommendations?"}}]},
    {"label": "RESPONSE", "pattern": [{"LOWER": "response"}]},
]

secondaries = [pattern["label"] for pattern in patterns]

for header in headers:
    pattern = {"label": "HEADER", "pattern": split_pattern(header)}
    patterns.append(pattern)

for cap in corrective_actions:
    pattern = {"label": "CORRECTIVE_ACTION", "pattern": split_pattern(cap)}
    patterns.append(pattern)


def expand_audit_numbers(doc):
    """
    We cannot use a conventional pipe here, because spacy sometimes
    parses 2xxx-yyy as a single entity (DATE or CARDINAL). Here, we
    explicitly match against a regexp and create custom spans; as
    such, this function _must_ be the first pipe executed, otherwise
    we will get overlapping entities for the same token.
    """
    new_ents = []
    for match in re.finditer("2\d{3}-\d{3}", doc.text):
        start, end = match.span()
        span = doc.char_span(start, end, label="AUDIT_NUMBER")
        if span is not None:
            new_ents.append(span)
    doc.ents = new_ents
    return doc


def sentences(doc, what):
    """
    Given a document with named entities, extract the sentence
    belonging to the named entity.
    """
    return [ent.sent for ent in doc.ents if ent.label_ == what]


def paragraphs(doc, what, startswith=False, experimental=False):
    """
    Given a document with named entities, extract the paragraph
    belonging to the named entity.
    """
    start = False
    overflow = 0
    current_audit = None
    current_sentence = ""
    sentences = []
    for sent in doc.sents:
        labels = [ent.label_ for ent in sent.ents]
        if "AUDIT_NUMBER" in labels:
            index = labels.index("AUDIT_NUMBER")
            current_audit = sent.ents[index].text
        if what in labels:
            if experimental:
                # experimental: if we have a secondary then we likely
                # accidentally hit the audit finding itself.
                if set(labels).intersection(set(secondaries)):
                    continue
            text = sent.text
            if startswith:
                index = labels.index(what)
                start = sent.ents[index].start
                text = doc[start : sent.end].text
            current_sentence = text
            start = True
            overflow = 0
        else:
            if start:
                if not "\n\n" in sent.text:
                    current_sentence += sent.text
                    overflow += 1
                else:
                    sentences.append((current_audit, clean(current_sentence)))
                    current_sentence = ""
                    start = False
                    overflow = 0
                if overflow > 20:
                    # prevent excessively large text dumps
                    sentences.append((current_audit, (clean(current_sentence))))
                    current_sentence = ""
                    start = False
                    overflow = 0
    return sentences


def extract_finding(doc, audit):
    """
    Given a header, examine the relevant context and see if we have
    a finding on our hands that corresponds to the given audit.
    """
    for sentence in sentences(doc, "HEADER"):
        for ent in doc.ents:
            if ent.start <= sentence.start:
                continue
            if ent.label_ in ["AUDIT_NUMBER"] and ent.text == audit:
                return clean(sentence.text)
    return None


def extract_cap(doc, audit):
    for (audit_match, cap_text) in paragraphs(
        doc, "CORRECTIVE_ACTION", startswith=True
    ):
        if audit_match == audit:
            return cap_text
    return None


def extract_findings(doc):
    return [sent.text for sent in sentences(doc, "HEADER")]


def get_secondaries(doc):
    results = []
    for ent in doc.ents:
        if ent.label_ in secondaries:
            sentence = clean(ent.sent.text.strip().split("\n\n")[0])
            results.append((ent.text, sentence))
    return results


def get_audit_numbers(doc):
    return {ent.text for ent in doc.ents if ent.label_ == "AUDIT_NUMBER"}


def results(doc):
    return [(ent.text.strip(), ent.label_) for ent in doc.ents]


def setup():
    nlp = spacy.load("en_core_web_sm")  # or 'en'
    ruler = EntityRuler(nlp, overwrite_ents=True)
    sentencizer = nlp.create_pipe("sentencizer")
    ruler.add_patterns(patterns)
    nlp.add_pipe(sentencizer, first=True)
    nlp.add_pipe(expand_audit_numbers, first=True)
    nlp.add_pipe(ruler)
    return nlp
