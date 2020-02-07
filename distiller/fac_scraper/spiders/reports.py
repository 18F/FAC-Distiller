import json
import os
import re

from django.conf import settings
from scrapy import FormRequest, Spider
from scrapy.exceptions import CloseSpider
from scrapy.utils.response import open_in_browser

from distiller.gateways import files
from ..items import FacSearchResultDocument


class FACSpider(Spider):
    name = 'fac'
    start_urls = ['https://harvester.census.gov/facdissem/SearchA133.aspx']
    download_delay = 1.5

    def __init__(
        self,
        *args,
        cfda=None,
        open_pages=False,
        **kwargs
    ):
        super(FACSpider, self).__init__(*args, **kwargs)

        # Set to open each search results page in a local browser, for
        # debugging purposes.
        self.open_pages = open_pages

        if not cfda:
            raise ValueError('A CFDA number/prefix is required')

        parts = cfda.split('.')
        if len(parts) > 2:
            raise ValueError('CFDA numbers are of the form XX.XXX')

        prefix = parts[0]
        if len(prefix) != 2:
            raise ValueError('CFDA prefix should be two digits')

        ext = parts[1] if len(parts) > 1 else None
        if ext and len(ext) > 3:
            raise ValueError('CFDA suffix should no more than three digits')

        wild = not (ext and len(ext) == 3)

        self.cfda_options = [{
            # Treat all queries as wildcards, with
            "Prefix": prefix,
            "Ext": ext,
            "Wild": wild

            # For reference, these attributes are also present on some
            # requests. (They may only be for the front-end's usage)
            # 'IsFullCFDAQuery': False,
            # "IsPrefixOnlyQuery": Flas,
            # 'IsExtensionOnlyQuery': False,
        }]

    def parse(self, response):
        # TODO: Determine how to parametize audit year and date ranges.
        return FormRequest.from_response(
            response,
            formdata={
                # Clear a few fields out that the site's Javascript must be
                # initializing on the real site:
                "ctl00$MainContent$UcSearchFilters$AuditeeEINs": "",
                "ctl00$MainContent$UcSearchFilters$AuditorEINs": "",

                # Audit year(s):
                #"ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$2": "2018",
                "ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$1": "2019",

                # Date range:
                #'ctl00$MainContent$UcSearchFilters$DateProcessedControl$FromDate': '09/01/2019',
                #'ctl00$MainContent$UcSearchFilters$DateProcessedControl$ToDate': '09/05/2019',

                # CFDA numbers:
                "ctl00$MainContent$UcSearchFilters$CDFASelectionControl$txtCfdaData": json.dumps(
                    self.cfda_options
                )
            },
            callback=self.parse_uniform_guidance_acknowledgement
        )

    def parse_uniform_guidance_acknowledgement(self, response):
        # We must agree to the "uniform guidance acknowledgement".
        return FormRequest.from_response(
            response,
            formdata={
                "ctl00$MainContent$chkAgree": "on"
            },
            callback=self.parse_row_datas
        )

    def parse_row_datas(self, response):
        """
        Toggle through each paginated search results page.
        """

        if self.open_pages:
            open_in_browser(response)

        # Find search result rows (tr) - Each results row has a download
        # checkbox.
        rows = response.xpath(
            '//table[@id="MainContent_ucA133SearchResults_ResultsGrid"]//td//span[starts-with(@id, "MainContent_ucA133SearchResults_ResultsGrid_EIN")]/../../..'
        )

        # We can extract structured data out of each search result row by
        # querying for input and span elements.
        # This will give us row data similar to:
        # {
        #     "ID": "1318542016",
        #     "VERSION": "2",
        #     "REPORTID": "02807677",
        #     "AUDITYEAR": "2016",
        #     "DBKEY": "131854",
        #     "DOWNLOAD": True,
        #     "EIN": "946000522",
        #     "FYENDDATE": "06/30/2016",
        #     "FACACCEPTEDDATE": "07/30/2019",
        #     "DATERECEIVED": "07/30/2019",
        # }
        for row in rows:
            row_data_common = {}

            # Extract values from input elements
            for elem in row.css('input'):
                if 'value' not in elem.attrib:
                    continue
                name = elem.attrib['name'].split('$')[-1]
                value = elem.attrib['value']
                if value in ('True', 'False'):
                    value = value == 'True'
                row_data_common[name] = value

            # Extract values from span elements
            for elem in row.css('span'):
                if 'id' not in elem.attrib:
                    continue
                name = elem.attrib['id'].split('_')[-2]
                value = elem.css('::text').extract_first()
                row_data_common[name] = value

            # The URLs are strings that look like this:
            # javascript:__doPostBack('ctl00$MainContent$ucA133SearchResults$ResultsGrid$ctl02$lnkbuttonForm','')
            # javascript:__doPostBack('ctl00$MainContent$ucA133SearchResults$ResultsGrid$ctl02$lnkbuttonAudit','')"
            for url in row.css('a[id]::attr(href)').extract():
                row_data = FacSearchResultDocument(**row_data_common)
                postback = self._extract_postback(url)

                # Get the file type
                # lnkbuttonForm or lnkbuttonAudit
                link_type = postback['event_target'].split('$')[-1]
                row_data['file_type'] = {
                    'lnkbuttonAudit': 'audit',
                    'lnkbuttonForm': 'form',
                }[link_type]

                # Construct the target file path
                ext = {
                    'lnkbuttonAudit': 'pdf',
                    'lnkbuttonForm': 'xlsx',
                }[link_type]
                file_name = f'{row_data["ID"]}{row_data["VERSION"]}.{ext}'
                row_data['file_path'] = os.path.join(
                    settings.FAC_DOCUMENT_DIR, file_name
                )

                # If the file has already been downloaded, yield the result.
                if os.path.exists(row_data['file_path']):
                    yield row_data

                # If the file has not been downloaded, download it and then
                # yield it.
                else:
                    yield self._do_post_back(
                        response,
                        **postback,
                        callback=self.save_attachment,
                        cb_kwargs={'row_data': row_data},
                    )

        # If there's a "next page", request it, recursing over this handler.
        next_page_postback_url = response.xpath(
            '//*[@class="GridPager"]//td/span/../following-sibling::td/a/@href'
        ).extract_first()
        if next_page_postback_url:
            yield self._do_post_back(
                response,
                **self._extract_postback(next_page_postback_url),
                callback=self.parse_row_datas
            )

    def save_attachment(self, response, *, row_data):
        """
        Save a PDF or Excel document from the given response.
        """

        # Get the file name from the headers
        #
        pattern = re.compile(r'attachment;filename="(?P<file_name>.*)"')
        match = pattern.match(response.headers['Content-Disposition'].decode())
        save_path = os.path.join(
            settings.FAC_DOCUMENT_DIR,
            match.group('file_name')
        )

        if row_data['file_path'] != save_path:
            # Raise this as CloseSpider to make the error visible - this would
            # indicate bad assumptions were made about the format of the
            # system's file names.
            raise CloseSpider(
                f'Unexpected file path: `{save_path}`, expected: `{row_data["file_path"]}`'
            )

        with files.output_file(save_path, 'wb') as out_file:
            out_file.write(response.body)

        yield row_data

    def _extract_postback(self, url):
        pattern = re.compile(r"javascript:__doPostBack\('(?P<event_target>.*)','(?P<event_argument>.*)'\)$")
        match = pattern.fullmatch(url)
        return {
            'event_target': match.group('event_target'),
            'event_argument': match.group('event_argument'),
        }

    def _do_post_back(self, response, *, event_target, event_argument, callback, cb_kwargs={}):
        """
        ASP VIEWSTATE is modified by a server callback, which looks like this:

            if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
                theForm.__EVENTTARGET.value = eventTarget;
                theForm.__EVENTARGUMENT.value = eventArgument;
                theForm.submit();
            }

        This function implements this logic in Python.
        """

        return FormRequest.from_response(
            response,
            # Set to prevent default form submit behavior
            dont_click=True,
            # Set to prevent Scrapy from filtering "duplicate" requests
            dont_filter=True,
            formdata={
                '__EVENTTARGET': event_target,
                '__EVENTARGUMENT': event_argument
            },
            callback=callback,
            cb_kwargs=cb_kwargs,
        )
