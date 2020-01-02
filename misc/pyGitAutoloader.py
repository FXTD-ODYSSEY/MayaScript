# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-02 15:41:11'

"""
自动重载线上的模块
"""

from maya import cmds
import os
import re
import sys
import imp
import subprocess

REMOTE = "9.134.117.16"

# NOTE 通过 git 读取更新日志
CMD = '//{REMOTE}/Tools/software/git/bin/git --git-dir //{REMOTE}/Tools/Scripts/.git show --pretty="" --name-only'.format(REMOTE=REMOTE)

cmds.progressWindow(title='读取更新信息',status="读取更新信息...",progress=0.0)

def runShellWithReturnCode(command,print_output=True,universal_newlines=True):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=universal_newlines)
    if print_output:
        output_array = []
        while True:
            line = p.stdout.readline()
            if not line:
                break
            output_array.append(line)
        output ="".join(output_array)
    else:
        output = p.stdout.read()
    p.wait()
    errout = p.stderr.read()
    if print_output and errout:
        return sys.stderr, errout
    p.stdout.close()
    p.stderr.close()
    return output, p.returncode

file_list,_ = runShellWithReturnCode(CMD,print_output=False,universal_newlines=False)


file_list = file_list.strip().split("\n")

cmds.progressWindow(e=1,title='重载模块',status="重载模块...",progress=10.0,isInterruptable=1 )

total = len(sys.modules)
for i,[name,module] in enumerate(sys.modules.items()):
    if cmds.progressWindow( q=1, isCancelled=1 ) :
		break
    if not module:
        continue

    for path in file_list:
        _,path = os.path.split(path)
        if path in str(module):
            cmds.progressWindow(e=1,status="重载：%s" % name,progress=float(i)/total*100)
            imp.reload(module)
    
    # # NOTE 查找路径是否含有 ip 地址
    # ip = re.search(r"((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}",str(module))
    # if ip and ip.group() == REMOTE:
    #     cmds.progressWindow(e=1,status="重载：%s" % name,progress=float(i)/total*100)
    #     imp.reload(module)

cmds.progressWindow(ep=1)