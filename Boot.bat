@echo off
SET EN=C:\Users\%username%\Pictures\Camera Roll\
SET JA=C:\Users\%username%\Pictures\�J���� ���[��\
@echo on

IF EXIST "%EN%" (
	move "%EN%*.jpg" %~dp0QRCode.jpg
) ELSE (
	move "%JA%*.jpg" %~dp0QRCode.jpg
)

python Main.py

@echo off
cmd /k
