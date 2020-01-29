"""
Filesystem operations supporting S3 and local filesystem
"""

import os
from glob import glob as stdlib_glob
from pathlib import Path
from typing import cast, Any, IO, List, Optional
from urllib.parse import urlparse

import requests
import s3fs
import smart_open


class FileOpenFailure(Exception):
    pass


def input_file(
    path: str, mode: str = 'r', encoding: Optional[str] = None
) -> IO[Any]:
    """
    Open a file for input purposes. Supports all filesystems supported by
    `smart_open`.
    """

    try:
        return cast(IO[Any], smart_open.open(path, mode, encoding=encoding))
    except:
        raise FileOpenFailure(f'Load failure: {path}')


def output_file(path: str, mode: str = 'w') -> IO[Any]:
    """
    Open a file for output purposes. Supports all filesystems supported by
    `smart_open`.
    """

    # If local file system, create directory if it doesn't exist.
    url = urlparse(path)
    if url.scheme == '':
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

    return cast(IO[Any], smart_open.open(path, mode))


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
        fs = s3fs.S3FileSystem(anon=False)
        return [
            f's3://{path}'
            for path in fs.glob(f'{bucket}{path}')
        ]

    # Assume filesystem path
    paths = sorted(f for f in stdlib_glob(path, recursive=True))

    return paths
