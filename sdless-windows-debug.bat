@echo off
:beginning
cd scripts
echo ^> python -m batchlinks-downloader.py --debug
echo.
python -m batchlinks-downloader.py --debug
echo.
echo Close the terminal to stop the looping launch
echo.
pause
echo.
goto beginning