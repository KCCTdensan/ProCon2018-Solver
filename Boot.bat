:move "C:\Users\%username%\Pictures\Camera Roll\*.jpg" %~dp0QRCode.jpg
move "C:\Users\%username%\Pictures\カメラ ロール\*.jpg" %~dp0QRCode.jpg

python Main.py

cmd /k
