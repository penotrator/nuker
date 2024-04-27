@echo off

title Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! (Go to https://www.python.org/downloads and install the latest version.^)
    echo Make sure it is added to PATH.
    goto ERROR
)

title Checking libraries...
echo Checking 'requests' (1/5)
python -c "import requests" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requests...
    python -m pip install requests > nul
)

echo Checking 'discord' (2/5)
python -c "import discord" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing discord...
    python -m pip install discord > nul
)

echo Checking 'colorama' (3/5)
python -c "import colorama" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing colorama...
    python -m pip install colorama > nul
)

echo Checking 'json' (4/5)
python -c "import json" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing json...
    python -m pip install json > nul
)

echo Checking 'pyfiglet' (5/5)
python -c "import pyfiglet" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pyfiglet...
    python -m pip install pyfiglet > nul
)

title Nuker

cls

pause

cd lib
python bot.py 
pause