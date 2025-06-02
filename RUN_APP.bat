@echo off
echo.
echo ==================================================
echo      Philosophical Universe Explorer
echo      Project Simone - AI-Powered Analysis
echo ==================================================
echo.
echo Starting the application...
echo.

REM Run the setup and launch script
python setup_and_run.py

REM If python command fails, try python3
if errorlevel 1 (
    echo.
    echo Trying with python3...
    python3 setup_and_run.py
)

REM If both fail, try py
if errorlevel 1 (
    echo.
    echo Trying with py launcher...
    py setup_and_run.py
)

if errorlevel 1 (
    echo.
    echo ==================================================
    echo ERROR: Python not found!
    echo.
    echo Please make sure Python 3.7+ is installed and
    echo added to your system PATH.
    echo.
    echo Visit: https://www.python.org/downloads/
    echo ==================================================
    pause
)