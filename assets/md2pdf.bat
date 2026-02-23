@echo off
REM md2pdf batch wrapper for Windows context menu
REM This handles quoted filenames properly

REM Remove quotes from the first argument (the filename)
set "filename=%~1"

REM Call the actual exe (unquoted args to avoid PyInstaller issue)
REM Update the path below to match your installation!
C:\Projects\md2pdf\dist\md2pdf.exe %filename%

