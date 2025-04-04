@echo off
setlocal enabledelayedexpansion

title pyrhythm song selector
chcp 65001 >nul
cls

REM Colors for the console
SET ESC=
SET BLUE=%ESC%[94m
SET RED=%ESC%[91m
SET GREEN=%ESC%[92m
SET RESET=%ESC%[0m


echo %BLUE%
echo "  ________  ___    ___ ________  ___  ___      ___    ___ _________  ___  ___  _____ ______      "
echo " |\   __  \|\  \  /  /|\   __  \|\  \|\  \    |\  \  /  /|\___   ___\\  \|\  \|\   _ \  _   \    "
echo " \ \  \|\  \ \  \/  / | \  \|\  \ \  \\\  \   \ \  \/  / ||___ \  \_\ \  \\\  \ \  \\\__\ \  \   "
echo "   \ \   ____\ \    / / \ \   _  _\ \   __  \   \ \    / /     \ \  \ \ \   __  \ \  \\|__| \  \  "
echo "    \ \  \___|\/  /  /   \ \  \\  \\ \  \ \  \   \/  /  /       \ \  \ \ \  \ \  \ \  \    \ \  \ "
echo "     \ \__\ __/  / /      \ \__\\ _\\ \__\ \__\__/  / /          \ \__\ \ \__\ \__\ \__\    \ \__\"
echo "      \|__||\___/ /        \|__|\|__|\|__|\|__|\___/ /            \|__|  \|__|\|__|\|__|     \|__|"
echo "         \|___|/                            \|___|/                                              
echo.


:: Define the charts folder
set "CHARTS_DIR=charts"

:: Check if charts folder exists
if not exist "%CHARTS_DIR%" (
    echo Error: "charts" folder not found!
    pause
    exit /b
)

:: Gather song folders
set "INDEX=1"
for /d %%S in (%CHARTS_DIR%\*) do (
    set "SONG_FOLDER=%%~nxS"
    set "SONG_NAME=!SONG_FOLDER:_= !"
    echo !INDEX!. !SONG_NAME!
    set "SONG_!INDEX!=!SONG_FOLDER!"
    set /a INDEX+=1
)

:: Adjust index for user input
set /a MAX_INDEX=%INDEX%-1

:: If no songs found, exit
if %MAX_INDEX% lss 1 (
    echo no songs found in "charts" folder.
    pause
    exit /b
)

:: Ask user to select a song
echo %RESET%
choice /c 1234567890 /n /m "select a song (1-%MAX_INDEX%): "
set "CHOICE_NUM=%ERRORLEVEL%"

:: Validate selection
if %CHOICE_NUM% gtr %MAX_INDEX% (
    echo invalid selection!
    pause
    exit /b
)

:: Get the selected song folder
for /l %%N in (1,1,%MAX_INDEX%) do (
    if %CHOICE_NUM%==%%N set "SELECTED=!SONG_%%N!"
)

:: Convert folder name back to readable format (replace underscores with spaces)
set "SONG_NAME=%SELECTED:_= %"

:: Save selection to selectedsong.txt
echo %SELECTED% > misc/selectedsong.txt

:: Confirm selection
echo selecting "%SONG_NAME%" to play...
echo %GREEN%written selection to "selectedsong.txt".%RESET%
echo %RED%launching pyrhythm...%RESET%

:: Run the Python game script
python3.13 pyrhythm.py
pause