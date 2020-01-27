"""
Tests for the load of FAC tables.
"""

import datetime
import os

from ..etls.single_audit_db import _yield_rows


def test_load_cdfa():
    table = _get_table_details()[1]
    csv_file = smart_open.open(table['url'], encoding='latin-1')
    _yield_rows(
        csv_file,
        table['field_mapping'],
        table['sanitizers'],
    )
