"""
Filesystem operations supporting S3 and local filesystem
"""

import os
from glob import glob as stdlib_glob
from pathlib import Path
from typing import cast, Any, IO, List, Optional
from urllib.parse import urlparse

import boto3
import s3fs
import smart_open
from django.conf import settings


class FileOpenFailure(Exception):
    pass


def _get_boto3_session():
    # Add AWS session credentials for S3
    return boto3.Session(
        aws_access_key_id=settings.S3_KEY_DETAILS['access_key_id'],
        aws_secret_access_key=settings.S3_KEY_DETAILS['secret_access_key'],
        region_name=settings.S3_KEY_DETAILS['region'],
    )


def _open(
    scheme: str, path: str, mode: str, encoding: Optional[str] = None, **kwargs
) -> IO[Any]:
    transport_params = None

    # If S3, create boto3 session with necessary credentials.
    if scheme == 's3':
        transport_params = {
            'session': _get_boto3_session()
        }

    return cast(IO[Any], smart_open.open(
        path,
        mode,
        encoding=encoding,
        transport_params=transport_params,
        **kwargs,
    ))


def input_file(
    path: str, mode: str = 'r', encoding: Optional[str] = None, **kwargs
) -> IO[Any]:

    """
    Open a file for input purposes. Supports all filesystems supported by
    `smart_open`.
    """

    url = urlparse(path)

    try:
        return _open(url.scheme, path, mode, encoding=encoding, **kwargs)
    except Exception as e:
        raise FileOpenFailure(f'Load failure: {path} with error {e}')


def output_file(path: str, mode: str = 'w') -> IO[Any]:
    """
    Open a file for output purposes. Supports all filesystems supported by
    `smart_open`.
    """

    url = urlparse(path)

    # If local file system, create directory if it doesn't exist.
    if url.scheme == '':
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

    return _open(url.scheme, path, mode)


def glob(path: str) -> List[str]:
    """
    Recursively glob for matching files over either a local file system or s3.
    Paths may include: **, *, ?
    Paths returned in standard alpha-numeric sort order.
    """
    url = urlparse(path)

    # If S3, use s3fs
    if url.scheme == 's3':
        # s3fs won't expand non-globs
        if not any(char in url.path for char in ('*', '?')):
            return [path]
        fs = s3fs.S3FileSystem(anon=False, session=_get_boto3_session())
        return [
            f's3://{path}'
            for path in fs.glob(f'{url.netloc}{url.path}')
        ]

    # Assume filesystem path
    paths = sorted(f for f in stdlib_glob(path, recursive=True))

    return paths


def exists(path: str) -> bool:
    url = urlparse(path)
    if url.scheme == 's3':
        fs = s3fs.S3FileSystem(anon=False)
        return fs.exists(path)
    return os.path.exists(path)
