@echo off
REM Thin launcher — all logic lives in update.py (next to this file). Double-click to update.
cd /d "%~dp0"

echo MedSci Skills Updater for Windows
echo.

python "%~dp0update.py" %*
set rc=%errorlevel%

if %rc% neq 0 (
  echo.
  echo If Python was not found, install Python 3 from https://www.python.org/downloads/ and run this updater again.
)

echo.
pause
exit /b %rc%
