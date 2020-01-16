# Distiller external data app

This Django app includes ETL, ORM models, and a data access interface for
external data used by the Federal Audit Clearinghouse Distiller.

## ETLs

- Put each data source's ETLs in a module in `./etls`.
- Create a Django management command in `./management/commands` to run the job.

## Use cases

Put data access use cases in `./access.py`
