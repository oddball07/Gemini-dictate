@echo off
rem Put this file in the SAME folder as gemini_widget.pyw and double-click it once.
rem   1. "dictate" in any terminal now opens gemini_widget.pyw (any old "dictate" command is renamed to *.old)
rem   2. gemini_widget.pyw starts automatically when you sign in to Windows (and opens Gemini hidden)
setlocal EnableExtensions

set "WIDGET=%~dp0gemini_widget.pyw"
if not exist "%WIDGET%" (
  echo gemini_widget.pyw must be in the same folder as this file.
  pause
  exit /b 1
)

set "PYW="
for /f "delims=" %%P in ('where pythonw 2^>nul') do if not defined PYW set "PYW=%%P"
if not defined PYW (
  echo Could not find pythonw.exe. Install Python and make sure it is added to PATH.
  pause
  exit /b 1
)

rem --- 1. the "dictate" command ---
for /f "delims=" %%F in ('where dictate 2^>nul') do ren "%%F" "%%~nxF.old" 2>nul

set "TARGET=%LOCALAPPDATA%\Microsoft\WindowsApps\dictate.cmd"
> "%TARGET%" echo @start "" "%PYW%" "%WIDGET%"
echo Created: %TARGET%

rem --- 2. start with Windows ---
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Startup')+'\Gemini Dictate.lnk'); $s.TargetPath='%PYW%'; $s.Arguments='\"%WIDGET%\"'; $s.WorkingDirectory='%~dp0'; $s.Save()"
echo Added to Windows startup.

echo.
echo Done. Open a NEW terminal and type: dictate
start "" "%PYW%" "%WIDGET%"
pause
