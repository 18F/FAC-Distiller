# Distiller

[Distiller](https://demo-fac-distiller.app.cloud.gov/), provides easier access to audit data. What is a multi-day process for some agencies has been reduced to a few minutes by helping  grant managers sorting through the Federal Audit Clearinghouse to identify the specific audits that they need to know have been completed and confirm if action needs to be taken by themselves or others. This tool is also helpful auditors, agency CFOs as well as grantees to be aware of audit activity happening by federal agency/sub agency.

This codebase spun out of the [10x Federal Grant Reporting Project](https://github.com/18F/federal-grant-reporting/) that is exploring simpler, faster, easier, better resolution of single audit findings by agencies and grantees alike.

**Features of the Distiller:**
- quickly match Assistance Listings (CFDA#s) from beta.sam.gov to parent and sub-agencies
- filter by agency/sub-agency, audits with findings, cognizant and oversight agencies and findings by agency filter
- sort by grantee name, # of findings, Fiscal year end,	Audit accepted date, name of	Cognizant or Oversight agency and whether or not an audit has	Questioned costs
- view only the findings for which your agency/sub-agency is Cognizant or Oversight for and responsible for resolving
- copy findings text and corrective action plans directly from the Distiller
- download a csv of your search results so you can process the data further or upload to an agency's case management system

Visit the [Distiller prototype](https://demo-fac-distiller.app.cloud.gov/)

### Audit PDF Extraction

This is a proof-of-concept module that is a companion to the Distiller. Download any audit pdf from the distiller and run it though this module that reads Single Audit PDFs page by page and extracts findings text and corrective action plans which can be viewed as a csv.

**This saves time** for grants managers searching for audit findings prior to fiscal year 2019 (before this was available in the Federal Audit Clearinghouse's Data Collection Form) and anyone who wants to take findings and corrective action plans text and copy them into another place.

**This reduces errors** We've heard that copying and pasting from audit pdfs is unreliable due to pdf formatting so agency staff have resorted to _retyping_ this information into their grants management tracking systems (which vary from spreadsheets to more robust case management systems). Retyping is prone to error in addition to taking away time from other tasks. Auditors and grantees who need to copy text of findings and corrective action plans into the Federal Audit Clearinghouse's Data Collection Form can more easily copy text from a csv instead of a poorly formatted or image pdf.

Results will vary with this tool as the text in these pdfs are no where near standardized and some older pdfs contain images instead of readable text which will limit any efforts to extract text from these PDFs. **We recommend updates to the policy for single audit format requirements** to require findings to be written in a standardized  format to make it easier and more reliable for them to be read by natural language processing and compared across audits for risk management.

See the [corresponding module for more details](https://github.com/18F/FAC-Distiller/tree/master/distiller/extraction/ "pdf extraction module README").

## How you can help

Visit the [Distiller prototype](https://demo-fac-distiller.app.cloud.gov/) on cloud.gov or test out the Single Audit PDF Extraction module and let us know if it useful or if something isn't working as expected. Email the team at federal-grant-reporting@gsa.gov or [File an issue](https://github.com/18F/FAC-Distiller/issues/new) and assign it to @bpdesigns.

## Local development

To develop against a Docker-based Postgres DB and a local virtual environment, follow these steps.

### Dependencies

1. Install [Docker][https://www.docker.com/]. If you're on OS X, install Docker for Mac. If you're on Windows, install Docker for Windows.

2. Install Python dependencies into a Pipenv-managed virtual environment

```shell
pipenv install --dev
```

NOTE: Python 3.7 is required.

### Local settings

Optionally, create a local settings file in `distiller/settings/local.py`:

```python
from .development import *

CHROME_DRIVER_LOCATION = os.path.join(BASE_DIR, 'chromedriver')
```

### Database server

To start a database server, run one of these commands:

```shell
# Run in the foreground
docker-compose up db
# Run in the background
docker-compose up -d db
```

#### Initialize database

Create database tables:

```shell
docker-compose run app python manage.py migrate
```

Create a Django admin user to access the admin interface:

```shell
docker-compose run app python manage.py createsuperuser
```

#### Start a development webserver

```shell
pipenv run manage.py runserver
```

Visit [http://localhost:8000/](http://localhost:8000/) directly to access the site.

You can access the admin panel at [http://localhost:8000/admin](http://localhost:8000/admin)
 by logging in with the super user credentials you created in the step above.

## Running ETLs

This application relies on external data sources. To populate the database with required data, run these ETL jobs.

### Download source tables

To load, first download the source table dumps. By default, these tables will be placed in timestamped directories under `/imports`. In production, these files will be placed in an S3 bucket.

To may download specific tables, or all tables at once.

```shell
pipenv run python manage.py download_table --all
pipenv run python manage.py download_table --audit
pipenv run python manage.py download_table --cfda
pipenv run python manage.py download_table --finding
pipenv run python manage.py download_table --findingtext
```

### Load tables

```shell
pipenv run python manage.py load_table --all
pipenv run python manage.py load_table --audit
pipenv run python manage.py load_table --cfda
pipenv run python manage.py load_table --finding
pipenv run python manage.py load_table --findingtext
```

### Cloud.gov jobs

In the deployed environment, `django-apscheduler` is used to refresh all tables daily at 12:00 AM EST.

At 1:00 AM EST, a complete crawl of the 2019 documents are completed, and then refreshed in the database.

NOTE: `django-apscheduler` is not an optimal choice for a cloud.gov deployment, because jobs are run in the same container as the web server. Usage of `cf run-task` would be preferred. Future work should involve scheduling tasks with `cf run-task` in an outside environment, such as a CircleCI periodic job.

### requirements.txt

To install the spacy English language pack (`en_core_web_sm`) on cloud.gov, we must explicitly specify this dependency as a file download in `requirements.txt` (see this [related spacy Github issue](https://github.com/explosion/spaCy/issues/3536 "spacy Github issue about installation of language models from pyPI"). Unfortunately, this also means maintaining Pipenv _and_ a requirements file.

When updating package versions, the `requirements.txt` can be re-generated by running `pipenv run pip freeze > requirements.txt`, removing the `en_core_web_sm` package line and then re-adding the `en_core_web_sm` https release link so that cloud.gov can install the language pack correctly.

### cf-service-connect

For local debugging, install [the cf service-connect plugin](https://github.com/18F/cf-service-connect "cf service connect plugin") and run `./bin/tunnel_cf_db` to access the postgres database
on cloud.gov.

## Scraping FAC documents

Scrapy is used to download documents from the Federal Audit Clearinghouse website.

Here are some example crawls:

```shell
# Crawl all documents from prior year with CFDA `11.*`
pipenv run scrapy crawl fac -a cfda=11

# Crawl all documents from prior year with CFDA `11.2*`
pipenv run scrapy crawl fac -a cfda=11.2

# Crawl all documents from prior year with CFDA `11.123`
pipenv run scrapy crawl fac -a cfda=11.123

# Crawl all documents from prior year with CFDA `11*`
# Also, for debugging, open a copy of each search results page in a browser.
pipenv run scrapy crawl fac -a cfda=11.123 -a open_pages=1
```

In production usage, metadata on these documents should be output to file, so it may be loaded into the Distiller database. Use the `-t` and `-o` Scrapy options to specify a format and target file name:

```shell
pipenv run scrapy crawl fac -a cfda=11.123 -t json -o test.json
```

There is a script checked into the repository that will assist in refreshing a subset of CFDA prefices on a cloud.gov deployment. To run as a one-off task:

```
cf run-task demo-fac-distiller "/home/vcap/app/bin/crawl"
```

## Deployment to cloud.gov

To expedite new deploys to cloud.gov, we provide a deployment script at [bin/setup-new-cf-instance.sh](https://github.com/18F/FAC-Distiller/blob/master/bin/setup-new-cf-instance.sh "shell script at bin/setup-new-cf-instance.sh"). Please note that you must be logged in cloud.gov or cloud foundry with the appropriate permissions to create an app and its associated services.

## Running tests

To run the test suite with `pytest`:

```shell
pipenv run pytest
```

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.


## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.

[Docker]: https://www.docker.com/
[http://localhost:8000/]: http://localhost:8000/
