# 10x Federal Grant Reporting Distiller Project

## Project description

### The 10x Federal Grant Reporting project is enabling simpler, faster, easier, better resolution of single audit findings by agencies and grantees alike.

To that end, we're building prospective shared solutions for the single audit finding resolution process.

### Distiller

Distiller, provides easier access to data, reducing a multi-day process to less than five minutes. This stands to help auditors, grant managers, and agency CFOs as well as grantees.

This codebase was extracted from exploritory work available [here](https://github.com/18F/federal-grant-reporting/).


## How can you help?

### Federal granting agency

If you're someone who works with single audits at a federal agency, we're interested in speaking with you.

Email the team at federal-grant-reporting@gsa.gov or [File an issue](https://github.com/18F/federal-grant-reporting/issues/new).

### Independent auditors

If you're someone who's created single audits, we're interested in talking with you and better understanding your current process and any pain points around creating audits and adding them to the Federal Audit Clearinghouse.

Email the team at federal-grant-reporting@gsa.gov or [File an issue](https://github.com/18F/federal-grant-reporting/issues/new).

### Grantees

If you've developed corrective action plans or been involved in single audit finding resolution, we'd love to talk.

Email the team at federal-grant-reporting@gsa.gov or [File an issue](https://github.com/18F/federal-grant-reporting/issues/new).


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

### Assistance listings from beta.sam.gov

```shell
pipenv run python manage.py load_assistance_listings
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
