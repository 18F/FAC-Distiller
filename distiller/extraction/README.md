# Extraction from audit PDFs

This module provides a proof of concept for extracting data from audit PDFs using [spacy](https://spacy.io/ "spacy, a natural language processing library").

There are two main items of interest we wish to extract from the PDF: all audit results (keyed with an audit number such as `2019-002`) and the corresponding corrective action plan, if any.

The general algorithm is as follows:

- For every page in the PDF document
  - Extract the corresponding text
  - Run NLP analysis to identify interesting sections
  - Convert section to a finding
    - Run heuristics over the section to identify the finding
      - Heuristics may reject the section
      - Heuristics may also try to clean up the data
    - Attempt to identify corresponding corrective action plan

Keywords are listed in `nlp.py`. For example, if we see an audit number next to `criteria or specific requirement` then we want to extract both bits of information together: the audit number and criteria.

## Caveats

Capturing and processing PDF text is necessarily a messy process. The audit PDFs can be in any format, and so over-capture of interesting results is an explicit design goal.

All pages in the PDF must be extractable. The code will reject any PDFs that are not marked as extractable or have text as images (OCR is beyond the scope of this project). The code will halt if any errors are encountered during the processing of the PDF.

Because we extract findings per page, any findings that run over one page may be duplicated in the output or result in missing information.

# Running as a module

You can run this module standalone:

    python -m distiller.extraction.analyze --help

This module accepts one parameter: the PDF file to process. By default, the results will be output to stdout. You can also specify `--csv` and `--pickle` to store the output as files with these respective formats. These options can also be used in conjunction with `--errors`, which will output the errors (if any) in the given format.

Required libraries are in `Pipfile` or `requirements.txt` in the root of this repository.

## Example run

    $ python -m distiller.extraction.analyze fac-documents/13404420191.pdf --csv test.csv
    processing fac-documents/13404420191.pdf
    processed fac-documents/13404420191.pdf with 16 results

    $ wc -l test.csv
    17 test.csv
