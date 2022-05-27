# -*- coding: utf-8 -*-
"""
clean up dayu_widgets 
`from dayu_widgets.qt import *`
convert this line to actual qt import 
base on pylint analysis
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-12-04 22:34:06"

import re
import os
import uuid
from collections import defaultdict
from io import StringIO
from pylint.reporters import text
from pylint.lint import Run
from Qt import QtCore, QtGui, QtWidgets
from multiprocessing.dummy import Pool

DIR = os.path.dirname(__file__)
TEMP = os.path.join(DIR, "temp")
not os.path.isdir(TEMP) and os.mkdir(TEMP)


def run_pylint(path, check):
    pylint_opts = [path, "-d", "all", "-e", check, "--reports=n"]
    pylint_output = StringIO()
    reporter = text.TextReporter(pylint_output)
    Run(pylint_opts, reporter=reporter, do_exit=False)
    return pylint_output.getvalue()


def get_qt_module(module):
    core = "QtCore" if getattr(QtCore, module, None) else ""
    gui = "QtGui" if getattr(QtGui, module, None) else ""
    widgets = "QtWidgets" if getattr(QtWidgets, module, None) else ""
    return core or gui or widgets


def fix_file(script_path):
    print("run: " + script_path)

    temp_path = os.path.join(TEMP, str(uuid.uuid4()))
    reg = re.compile(r"^.+:(\d+?):(\d+?):.*?'(\D+?)'")
    output = run_pylint(script_path, "no-name-in-module")
    num_list = []
    lines = []
    with open(script_path, "r", encoding="utf8") as f:
        lines = f.readlines()

    for i, line in enumerate(output.splitlines()):
        match = reg.match(line)
        if match:
            # print(line)
            line_num = match.group(1)
            num_list.append(int(line_num) - 1)

    for i in reversed(num_list):
        del lines[i]

    del num_list[:]

    if "from dayu_widgets.qt import *\n" in lines:
        i = lines.index("from dayu_widgets.qt import *\n")
        del lines[i]
    with open(temp_path, "w", encoding="utf8") as f:
        f.write("".join(lines))

    output = run_pylint(temp_path, "undefined-variable")

    num_dict = defaultdict(list)
    for i, line in enumerate(output.splitlines()):
        match = reg.match(line)
        if match:
            print(line)
            line_num = match.group(1)
            start = match.group(2)
            module = match.group(3)
            num_dict[int(line_num) - 1].append((int(start), module))

    qt_modules = set()
    for num, infos in num_dict.items():
        offset = 0
        for start, module in infos:
            start += offset
            line = lines[num]
            pre_line = line[:start]
            post_line = line[start + len(module) :]
            qt_module = get_qt_module(module)
            qt_modules.add(qt_module)
            assert qt_module, "empty qt module -> " + module
            offset += len(qt_module) + 1
            module = qt_module + "." + module
            line = pre_line + module + post_line
            lines[num] = line

    if not qt_modules:
        return
    i = lines.index("from __future__ import print_function\n")
    lines.insert(i + 1, "from Qt import %s\n" % ",".join(qt_modules))
    # with open(temp_path, "w", encoding="utf8") as f:
    with open(script_path, "w", encoding="utf8") as f:
        f.write("".join(lines))


def main():
    errors = []
    path = os.path.join(DIR, "examples")
    paths = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if not f.endswith("py") or f == "__init__.py":
                continue
            script_path = os.path.join(root, f)
            paths.append(script_path)

    # pool = Pool(8)
    # pool.map(fix_file,paths)
    paths = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.endswith(".py") and not f == "__init__.py"
    ]

    for script_path in paths:
        try:
            fix_file(script_path)
        except:
            errors.append(script_path)

    print("\n====errors=====\n")
    print("\n".join(errors))


if __name__ == "__main__":
    # main()
    fix_file(r"f:/repo/dayu_widgets\examples\check_box_group_example.py")
