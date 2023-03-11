@echo off
:beginning
cd scripts
echo ^> python -m batchlinks-downloader.py
echo.
python -m batchlinks-downloader.py
echo.
echo Close the terminal to stop the looping launch
echo.
pause
echo.
goto beginning