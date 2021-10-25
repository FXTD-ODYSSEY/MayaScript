@echo off
@REM 输入 github 仓库会自动 clone 并等待 1s 用 vscode 打开这个路径

@REM 获取粘贴板的信息
set cliptext=%temp%\__clone_cliptext__
if exist "%cliptext%" del "%cliptext%"
powershell -sta "add-type -as System.Windows.Forms; [windows.forms.clipboard]::GetText()" >> %cliptext%
for /f %%i in (%cliptext%) do set repo=%%i

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

