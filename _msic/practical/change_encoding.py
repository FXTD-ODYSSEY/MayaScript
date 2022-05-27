# -*- coding: utf-8 -*-
"""
glob match specific files convert to utf-8 encoding
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
from functools import reduce
import glob
from operator import add
import os

# Import third-party modules
import chardet


def change_encoding(path, encoding="utf-8"):
    rawdata = open(path, "rb").read()
    file_encoding = chardet.detect(rawdata)["encoding"]
    if file_encoding != encoding:
        with open(path, "w", encoding=encoding) as wf:
            wf.write(rawdata.decode(file_encoding))


def glob_files(ext):
    DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(DIR, "**/*.{0}".format(ext))
    return glob.glob(path, recursive=True)


def iterate_files(ext_list):
    for path in reduce(add, map(glob_files, ext_list)):
        yield path


if __name__ == "__main__":
    for path in iterate_files(["cpp", "h", "md"]):
        change_encoding(path)
