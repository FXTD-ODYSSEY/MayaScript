# -*- coding: utf-8 -*-
"""
https://developpaper.com/svn-e155010-pristine-text-a31e85c8d4-089ed435e-not-present
https://gist.github.com/mcbrwr/4e04cee615bd954476cd
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-09-17 16:34:36'

import os
import re
import sys
import subprocess

DIR = os.path.dirname(__file__)
sqlite3 = os.path.join(DIR,'sqlite3')
db = os.path.join(DIR,'.svn','wc.db')
# svn = r"F:\RED\RedApp\RedTools\svnCommandLine\svn"
svn = r"svn"

def svn_cleanup():
    p = subprocess.Popen([svn,'update'],stderr=subprocess.PIPE,cwd=DIR,shell=True)
    p.wait()
    err_text = p.stderr.read()
    print(err_text)
    
    matches = re.findall(r" '(.*)' ",str(err_text))
    if not matches:
        return
    return matches[-1]

match = svn_cleanup()
# # print("match",match)
# while match:
#     print(match)
#     command = "UPDATE nodes set presence='not-present' WHERE checksum like '%{}'".format(match) 
#     command = ' '.join([sqlite3,db,'"%s"' % command])
#     print(command)
#     subprocess.call(command,shell=True)
#     match = svn_cleanup()

# select local_relpath from nodes where checksum=""