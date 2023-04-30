@echo off
if exist gradioinstalled.bak goto beginning
echo Checking gradio version...
echo.
python -c "import gradio" 2>nul && (
    python -c "import gradio; assert gradio.__version__ == '3.16.2'" 2>nul || (
        pip install gradio==3.16.2
    )
) || (
    pip install gradio==3.16.2
)
pip show tqdm >nul || pip install tqdm
pip freeze | findstr /i "\<gradio\>" >nul && pip freeze | findstr /i "\<tqdm\>" >nul && (echo. > gradioinstalled.bak)
echo.

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