@echo off

@REM ::administartor
@REM mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c rez python %~dp0rps.py %* ","","runas",1)(window.close)


rez python %~dp0rps.py %*

