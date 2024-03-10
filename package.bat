@echo off
echo y | pyinstaller --windowed --add-data "assets;assets" --add-data "image;image" --add-data "icon.ico;." --icon=icon.ico app.py
pause