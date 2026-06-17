@echo off
chcp 1251 > nul
setlocal enabledelayedexpansion

echo ===================================================
echo   Onovlennya ta zavantazhennya lokalizacii v Steam
echo ===================================================
echo.

:: 1. Copy files
set "SRC_DIR=C:\Users\cakam\Documents\GitHub\GloomHavenUa"
set "DEST_DIR=C:\Users\cakam\AppData\LocalLow\FlamingFowlStudios\Gloomhaven\SteamMods\UkraineHaven"

echo [1/3] Kopiuvannya fajliv lokalizacii...
echo Dzherelo: %SRC_DIR%\LangPacks
echo Cil:    %DEST_DIR%\LangPacks
echo.

if not exist "%DEST_DIR%\LangPacks" mkdir "%DEST_DIR%\LangPacks"

copy /Y "%SRC_DIR%\gloom.mod" "%DEST_DIR%\" > nul
copy /Y "%SRC_DIR%\thumbnail.png" "%DEST_DIR%\" > nul
xcopy /E /I /Y "%SRC_DIR%\LangPacks" "%DEST_DIR%\LangPacks" > nul

if %ERRORLEVEL% equ 0 (
    echo [OK] Fajly uspisno skopiyovano!
) else (
    echo [ERROR] Pomylka kopiuvannya fajliv.
    pause
    exit /b %ERRORLEVEL%
)
echo.

:: 2. Credentials
echo [2/3] Vvedit login Steam:
set /p STEAM_USER="Login: "

:: VDF File
set "VDF_FILE=%SRC_DIR%\steamcmd\workshop_upload.vdf"
(
echo "workshopitem"
echo {
echo   "appid" "780290"
echo   "publishedfileid" "3400827393"
echo   "contentfolder" "%DEST_DIR%"
echo   "changenote" "Localization update"
echo }
) > "%VDF_FILE%"

echo.
echo [3/3] Zapusk zavantazhennya v Steam Workshop...
echo.

"%SRC_DIR%\steamcmd\steamcmd.exe" +login "%STEAM_USER%" +workshop_build_item "%VDF_FILE%" +quit

:: Delete temp VDF
if exist "%VDF_FILE%" del "%VDF_FILE%"

echo.
echo ===================================================
echo Process zaversheno.
echo ===================================================
pause
