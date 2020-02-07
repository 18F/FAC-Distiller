# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FacSearchResultDocument(scrapy.Item):
    """
    One document from FAC search results.
    There could 0-2 documents per audit search result.

    This item type stores the common fields on each document to make handling
    duplicates straightforward.

    Example data:
        {'AUDITYEAR': '2016',
         'DATERECEIVED': '07/30/2019',
         'DBKEY': '131854',
         'DOWNLOAD': True,
         'EIN': '946000522',
         'FACACCEPTEDDATE': '07/30/2019',
         'FYENDDATE': '06/30/2016',
         'ID': '1318542016',
         'REPORTID': '02807677',
         'VERSION': '2',
         'file_path': '/Users/dan/src/10x/fac-scraper/audit_documents/13185420162.xlsx',
         'file_type': 'form'}
    """

    # Fields extract from search results row
    ID = scrapy.Field()
    VERSION = scrapy.Field()
    REPORTID = scrapy.Field()
    AUDITYEAR = scrapy.Field()
    DBKEY = scrapy.Field()
    DOWNLOAD = scrapy.Field()
    EIN = scrapy.Field()
    FYENDDATE = scrapy.Field()
    FACACCEPTEDDATE = scrapy.Field()
    DATERECEIVED = scrapy.Field()

    # Document details.
    # file_type is "form" or "audit"
    file_type = scrapy.Field()
    file_path = scrapy.Field()
