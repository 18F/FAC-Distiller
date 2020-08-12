from django.db import models


class ETLLogManager(models.Manager):
    def log_download_table(self, table_name):
        return self.create(
            operation='download_table',
            target=table_name,
        )

    def log_load_table(self, table_name):
        return self.create(
            operation='load_table',
            target=table_name,
        )

    def log_fac_document_crawl(self, crawl_parameters):
        return self.create(
            operation='fac_crawl',
            target=crawl_parameters,
        )

    def get_most_recent_load_table(self):
        return self.filter(operation='load_table').order_by('-created').first()

    def get_most_recent_document_crawl(self):
        return self.filter(operation='fac_crawl').order_by('-created').first()



class ETLLog(models.Model):
    """
    Track logs of data ingest operations.
    """

    objects = ETLLogManager()

    created = models.DateTimeField(auto_now_add=True)
    operation = models.CharField(max_length=16, choices=(
        ('load_table', 'Load table'),
        ('download_table', 'Download table'),
        ('fac_crawl', 'FAC document crawl'),
    ))
    target = models.CharField(max_length=128)
