@echo off
@REM 输入 github 仓库会自动 clone 并等待 1s 用 vscode 打开这个路径
@REM 如果 cmd 找不到 powershell 请将  %SYSTEMROOT%\System32\WindowsPowerShell\v1.0\ 加到 %PATH% 

@REM 获取粘贴板的信息
for /f "eol=; tokens=*" %%I in ('powershell Get-Clipboard') do set repo=%%I

echo "clone %repo%"

@REM 截取 repo url / 后的信息
set str=%repo%
set remain=%repo%
:loop
for /f "tokens=1* delims=/" %%a in ("%remain%") do (
	set name=%%a
	set remain=%%b
)
if defined remain goto :loop

@REM 用 vscode 打开路径
set folder=%name:~0,-4%
if exist "%folder%" rmdir /s /q "%folder%"
start /min cmd /c "TIMEOUT /T 1 & code %folder%"

git clone %repo%

