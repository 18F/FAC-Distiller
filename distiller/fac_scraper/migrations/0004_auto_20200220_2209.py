# Generated by Django 3.0.3 on 2020-02-20 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fac_scraper', '0003_auto_20200220_2148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facdocument',
            options={'ordering': ('dbkey', 'audit_year')},
        ),
    ]
