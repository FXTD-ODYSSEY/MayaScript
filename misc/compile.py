# -*- coding: utf-8 -*-
"""
快速编译 ui 生成兼容 Qt.py 的 ui 文件
只支持 Maya 2016 以上的版本 (没有做 pyside 兼容)
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-12-04 10:50:02"

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import os
import sys
import glob
import json
import string
import tempfile
import subprocess


DIR = os.path.dirname(__file__)


def get_maya_directory():
    for drive in string.ascii_uppercase:
        for path in glob.iglob(r"%s:\**\bin\maya.exe" % drive, recursive=True):
            uic = os.path.join(path, "..", "pyside2-uic")
            maya_dir = os.path.abspath(os.path.join(path, "..", ".."))
            if os.path.exists(uic) and os.path.exists(maya_dir):
                return maya_dir


class CompileUI(object):
    # def __init__(self):
    #     pass

    def get_maya_dir(self):
        temp_dir = tempfile.gettempdir()
        config = os.path.join(temp_dir, "compile_ui_maya_dir.json")
        maya_dir = ""
        if os.path.exists(config):
            with open(config) as f:
                try:
                    config = json.loads(f)
                    maya_dir = config.get("maya_dir")
                except:
                    pass

        if not maya_dir:
            maya_dir = get_maya_directory()
            obj = {"maya_dir": str(maya_dir)}
            with open(config, "w") as f:
                json.dump(obj, f)
        maya_py = os.path.join(maya_dir, "bin", "mayapy.exe")
        return maya_py

    def launch_mayapy_process(self):
        maya_py = self.get_maya_dir()
        subprocess.call([maya_py, __file__, "watch"], shell=True)

    def watch_file(self):
        from PySide2 import QtWidgets
        from PySide2 import QtCore

        bin = os.path.dirname(sys.executable)
        self.uic = os.path.join(bin, "pyside2-uic")

        watcher = QtCore.QFileSystemWatcher()

        for ui in os.listdir(DIR):
            if ui.endswith(".ui"):
                watcher.addPath(os.path.join(DIR, ui))

        watcher.fileChanged.connect(self.on_file_change)

        app = QtWidgets.QApplication(sys.argv)
        app.exec_()

    def on_file_change(self, path):
        directory, base = os.path.split(path)
        name = os.path.splitext(base)[0]
        ui_py = os.path.join(directory, "%s_ui.py" % name)
        subprocess.call(
            [
                sys.executable,
                self.uic,
                "-o",
                ui_py,
                path,
            ]
        )

        self.convert(ui_py)
        # print("file",sys.executable)

    def _convert(self, lines):
        """copy from Qt.py"""
        def parse(line):
            line = line.replace("from PySide2 import", "from Qt import QtCompat,")
            line = line.replace(
                "QtWidgets.QApplication.translate", "QtCompat.translate"
            )
            if "QtCore.SIGNAL" in line:
                raise NotImplementedError(
                    "QtCore.SIGNAL is missing from PyQt5 "
                    "and so Qt.py does not support it: you "
                    "should avoid defining signals inside "
                    "your ui files."
                )
            return line

        return [parse(line) for line in lines]

    def convert(self, file_path):
        """copy from Qt.py"""
        with open(file_path) as f:
            lines = self._convert(f.readlines())

        with open(file_path, "w") as f:
            f.write("".join(lines))


if __name__ == "__main__":
    compiler = CompileUI()
    if len(sys.argv) > 1:
        compiler.watch_file()
    else:
        compiler.launch_mayapy_process()

