# -*- coding: utf-8 -*-
"""
rps rez powershell command

# prefix for special command.

examples:
rps #code  -  activate env launch vscode
rps cmake maya  - activate powsershell with cmake&maya rez package
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-10-25 14:23:43"


# Import built-in modules
import logging
import os
import pathlib
import subprocess
import sys

# Import third-party modules
from rez import serialise

logging.basicConfig(level=logging.INFO)
ROOT = pathlib.Path(os.getcwd())

REZ_ENV = ["rez", "env", "--shell", "powershell"]


def build_sym(req):
    package = ROOT / "package.py"
    if not package.exists():
        return
    
    build_command = " ".join(["rez", "build", "--i", "--symlink"])
    logging.info(build_command)
    subprocess.call(build_command, shell=True)
    
    pkg = serialise.load_from_file(str(package))
    userprofile = pathlib.Path(os.getenv("userprofile"))
    package_path = userprofile / "packages" / pkg.get("name")
    package_version = package_path /pkg.get("version")
    logging.info(package_version)
    if package_version.exists():
        package_version.rename(str(package_path/ '999.0.0'))


COMMANDS = {
    "#code": lambda req: REZ_ENV + [*req, "--", "code", str(ROOT)],
    "#mobu": lambda req: REZ_ENV + [*req, "motionbuilder-2018", "--", "motionbuilder"],
    "#sym": build_sym,
}


def main():
    requires = []
    package = ROOT / "package.py"
    if package.exists():
        pkg = serialise.load_from_file(str(package))
        requires += pkg.get("requires", [])
        requires += pkg.get("build_requires", [])

    args = sys.argv[1:]
    requires += args

    for index, arg in enumerate(requires):
        if not arg.startswith("#"):
            continue
        post_args = requires[index + 1 :]
        requires = requires[:index]
        # not requires and requires.append("python")
        callback = COMMANDS.get(arg)
        requires = callback(requires) if callback else requires
        if requires is None:
            return
        requires += post_args
        command = " ".join(requires)
        break
    else:
        command = " ".join(REZ_ENV + requires)

    logging.info(command)
    subprocess.run(command)


if __name__ == "__main__":
    main()
