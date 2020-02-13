from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, resolve1
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import os
from io import StringIO

from ..gateways import files


def errors(fd):
    """
    Check that the PDF is extractable and that all pages can be converted to text.
    """
    errors = []
    page_number = 0
    parser = PDFParser(fd)
    document = PDFDocument(parser)
    if not document.is_extractable:
        errors.append("Warning: PDF is not extractable")
    for page in PDFPage.get_pages(fd):
        page_number += 1
        if not "Font" in page.resources.keys():
            errors.append(f"Warning: PDF page {page_number} has no text")
    return errors


def page_length(fd):
    """
    Get the page length of the given PDF.
    """
    parser = PDFParser(fd)
    document = PDFDocument(parser)
    return resolve1(document.catalog["Pages"])["Count"]


def page(fd, page_number):
    """
    Given a PDF and a page number, extract the text.
    """
    resource = PDFResourceManager()
    string = StringIO()
    device = TextConverter(resource, string, codec="utf-8", laparams=LAParams())
    interpreter = PDFPageInterpreter(resource, device)
    kwargs = {
        "maxpages": 0,
        "password": "",
        "caching": True,
        "check_extractable": False,
    }
    all_pages = PDFPage.get_pages(fd, set(), **kwargs)
    for index, page in enumerate(all_pages):
        if index == page_number:
            interpreter.process_page(page)
    text = string.getvalue()
    device.close()
    string.close()
    return text


def page_cached(fd, filename, page_number):
    """
    Cache PDF text if it exists: this speeds up program execution.
    """
    text_filename = f"{filename}.{page_number}.txt"
    if not os.path.isfile(text_filename):
        text = page(fd, page_number)
        with open(text_filename, "w") as fd:
            fd.write(text)
    return "".join(open(text_filename, "r").readlines())


def all_pages(fd):
    """
    Given a PDF, extract the text per page.
    """
    resource = PDFResourceManager()
    string = StringIO()
    device = TextConverter(resource, string, codec="utf-8", laparams=LAParams())
    interpreter = PDFPageInterpreter(resource, device)
    kwargs = {
        "maxpages": 0,
        "password": "",
        "caching": True,
        "check_extractable": False,
    }
    pages = []
    all_pages = PDFPage.get_pages(fd, set(), **kwargs)
    for index, page in enumerate(all_pages):
        interpreter.process_page(page)
        text = string.getvalue()
        pages.append(dict(page_number=index, text=text))
    device.close()
    string.close()
    return pages
