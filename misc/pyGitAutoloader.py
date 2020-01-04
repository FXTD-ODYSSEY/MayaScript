# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-02 15:41:11'

"""
更具git的更新文件 自动重载python的模块 | 并更新工具架
"""

from maya import cmds
from maya import mel
import os
import re
import sys
import imp
import subprocess

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


def main():
        
    REMOTE = "9.134.117.16"
    GIT_DIR = "//{REMOTE}/Tools/Scripts/".format(REMOTE=REMOTE)
    # NOTE 通过 git 读取更新日志
    # NOTE https://stackoverflow.com/questions/424071/how-to-list-all-the-files-in-a-commit
    # NOTE https://stackoverflow.com/questions/16792737/git-change-working-directory
    CMD = '//{REMOTE}/Tools/software/git/bin/git --git-dir //{REMOTE}/Tools/Scripts/.git show --pretty="" --name-only'.format(REMOTE=REMOTE)

    cmds.progressWindow(title=u'读取更新信息',status=u"读取更新信息...",progress=0.0)

    file_list,_ = runShellWithReturnCode(CMD,print_output=False,universal_newlines=False)

    file_list = file_list.strip().split("\n")
    py_list = filter(lambda x:x.endswith(".py"),file_list)
    mel_list = filter(lambda x:x.endswith(".mel"),file_list)


    cmds.progressWindow(e=1,title=u'重载模块',status=u"重载模块...",progress=30.0,isInterruptable=1 )

    total = len(sys.modules)
    for i,[name,module] in enumerate(sys.modules.items()):
        if cmds.progressWindow( q=1, isCancelled=1 ) :
            break
        if not module:
            continue

        for path in py_list:
            _,path = os.path.split(path)
            if path in str(module):
                cmds.progressWindow(e=1,status=u"重载：%s" % name,progress=float(i)/total*60+30)
                imp.reload(module)
        
        # # NOTE 查找路径是否含有 ip 地址
        # ip = re.search(r"((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}",str(module))
        # if ip and ip.group() == REMOTE:
        #     cmds.progressWindow(e=1,status="重载：%s" % name,progress=float(i)/total*100)
        #     imp.reload(module)


    mel_count = len(mel_list)

    if mel_count > 0:
            
        cmds.progressWindow(e=1,title=u'重载shelf',status=u"重载shelf...",progress=90.0)

        gShelfTopLevel = mel.eval("$temp = $gShelfTopLevel")
        shelves = cmds.shelfTabLayout(gShelfTopLevel,q=1,ca=1)
        index = cmds.shelfTabLayout(gShelfTopLevel,q=1,selectTabIndex=1)

        for j,m in enumerate(mel_list):
            for i,shelf in enumerate(shelves):
                if "shelf_" + shelf in m:
                    break
            else:
                continue

            cmds.progressWindow(e=1,title=u'重载shelf',status=u"重载shelf...",progress=float(j)/mel_count*10+90)
                    

            shelf_path = os.path.join(GIT_DIR,m).replace("\\","/")
            
            # NOTE 删除工具架
            cmds.deleteUI("%s|%s" % (gShelfTopLevel,"OP"),layout=1)
            # NOTE 创建工具架
            mel.eval('loadNewShelf("%s")' % shelf_path)
            curr = cmds.shelfTabLayout(gShelfTopLevel,q=1,numberOfChildren=1)
            cmds.shelfTabLayout(gShelfTopLevel,e=1,moveTab=[curr,i])

        # NOTE 切换回原来的 index
        cmds.shelfTabLayout(gShelfTopLevel,e=1,selectTabIndex=index)

        mel.eval('shelfTabChange')


    cmds.progressWindow(ep=1)

if __name__ == "__main__":
    main()