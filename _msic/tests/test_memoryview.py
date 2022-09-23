# -*- coding: utf-8 -*-
"""
Test Split data performance
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-09-08 16:48:47"

import time

# NOTES(timmyliang): 100 M data
bin_data = b"\x00" * 1024 * 1024 * 100


def log_time(func):
    def decorator(*args, **kwargs):
        curr = time.time()
        res = func(*args, **kwargs)
        print("[{0}] elapsed time: {1}".format(func.__name__, time.time() - curr))
        return res

    return decorator


@log_time
def test_memoryview(bin_data):
    bin_data = memoryview(bin_data)
    for index in range(100):
        bin_data[index:]


@log_time
def test_char(bin_data):
    for index in range(100):
        bin_data[index:]


if __name__ == "__main__":
    test_memoryview(bin_data)
    test_char(bin_data)
