@echo off
echo Set WshShell = CreateObject("WScript.Shell") > "%temp%\run_hidden.vbs"
echo WshShell.Run "pythonw run.py", 0, False >> "%temp%\run_hidden.vbs"
cscript //nologo "%temp%\run_hidden.vbs" & del "%temp%\run_hidden.vbs"
exit