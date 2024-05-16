@echo off

@REM 管理员权限启动脚本
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"

@REM 获取剪贴板数据
for /f "eol=; tokens=*" %%I in ('powershell Get-Clipboard') do set CLIPBOARD_TEXT=%%I
if "%CLIPBOARD_TEXT:~0,24%" equ "https://www.youtube.com/" yt-dlp -f bestvideo+bestaudio --external-downloader aria2c.exe --external-downloader-args "-x 16 -k 10M" %CLIPBOARD_TEXT% 
