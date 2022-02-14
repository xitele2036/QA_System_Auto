@echo off

if exist dist (
	echo del dist
	rmdir /s/q dist
	echo Done
	
	echo del build
	rmdir /s/q build
	echo Done
	goto package
	) else (
	goto package	
	)

:package
echo build package cmd
"C:\Users\kliu\AppData\Local\Programs\Python\Python39\Scripts\pyinstaller.exe" -D -i V.ico AutoTestApp.py
echo Done