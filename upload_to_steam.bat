@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ===================================================
echo     Gloomhaven Ukrainian Translation Updater
echo ===================================================
echo.

:: 1. Copy files
set "SRC_DIR=C:\Users\cakam\Documents\GitHub\GloomHavenUa"
set "DEST_DIR=C:\Users\cakam\AppData\LocalLow\FlamingFowlStudios\Gloomhaven\SteamMods\UkraineHaven"
set "NOTES_FILE=%SRC_DIR%\release_notes.txt"

if not exist "%NOTES_FILE%" (
    type NUL > "%NOTES_FILE%"
    echo [INFO] Created empty release_notes.txt
)

echo [1/3] Copying localization files...
echo Source: %SRC_DIR%\LangPacks
echo Target: %DEST_DIR%\LangPacks
echo.

if not exist "%DEST_DIR%\LangPacks" mkdir "%DEST_DIR%\LangPacks"

copy /Y "%SRC_DIR%\gloom.mod" "%DEST_DIR%\" > nul
copy /Y "%SRC_DIR%\thumbnail.png" "%DEST_DIR%\" > nul
copy /Y "%SRC_DIR%\thumbnail.png" "%DEST_DIR%\preview.png" > nul
xcopy /E /I /Y "%SRC_DIR%\LangPacks" "%DEST_DIR%\LangPacks" > nul

if %ERRORLEVEL% equ 0 (
    echo [OK] Files copied successfully!
) else (
    echo [ERROR] Failed to copy files.
    pause
    exit /b %ERRORLEVEL%
)
echo.

:: 2. Credentials
echo [2/3] Enter Steam login:
set /p STEAM_USER="Login: "

:: 3. Prepare VDF File
set "VDF_FILE=%SRC_DIR%\steamcmd\workshop_upload.vdf"
set "PREVIEW_FILE=%DEST_DIR%\preview.png"

powershell -ExecutionPolicy Bypass -File "%SRC_DIR%\steamcmd\prepare_upload.ps1" -NotesFile "%NOTES_FILE%" -DestDir "%DEST_DIR%" -PreviewFile "%PREVIEW_FILE%" -VdfFile "%VDF_FILE%"

if exist "%NOTES_FILE%" (
    for %%I in ("%NOTES_FILE%") do set FILE_SIZE=%%~zI
    if !FILE_SIZE! gtr 0 (
        echo [INFO] Loaded release notes from release_notes.txt
    ) else (
        echo [INFO] No custom release notes found, using default note.
    )
)

echo.
echo [3/3] Starting Steam Workshop upload...
echo.

"%SRC_DIR%\steamcmd\steamcmd.exe" +login "%STEAM_USER%" +workshop_build_item "%VDF_FILE%" +quit

set UPLOAD_ERROR=%ERRORLEVEL%

:: Delete temp VDF
if exist "%VDF_FILE%" del "%VDF_FILE%"

if %UPLOAD_ERROR% equ 0 (
    echo.
    echo [OK] Upload completed successfully!
    if exist "%NOTES_FILE%" (
        type NUL > "%NOTES_FILE%"
        echo [INFO] Cleared release_notes.txt to prevent duplicate uploads.
    )
) else (
    echo.
    echo [ERROR] SteamCMD upload failed with error code %UPLOAD_ERROR%.
)

echo.
echo ===================================================
echo Process completed.
echo ===================================================
pause
