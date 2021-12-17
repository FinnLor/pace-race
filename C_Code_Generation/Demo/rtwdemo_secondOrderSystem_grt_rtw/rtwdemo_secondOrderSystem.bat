@echo off

set skipSetupArg=%2
if "%skipSetupArg%" NEQ "skip_setup_msvc" (
call "setup_msvc.bat"
)

cd .

chcp 1252

if "%1"=="" (nmake  -f rtwdemo_secondOrderSystem.mk all) else (nmake  -f rtwdemo_secondOrderSystem.mk %1)
@if errorlevel 1 goto error_exit

exit /B 0

:error_exit
echo The make command returned an error of %errorlevel%
exit /B 1