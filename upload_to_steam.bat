@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ===================================================
echo   Оновлення та завантаження локалізації в Steam
echo ===================================================
echo.

:: 1. Копіюємо оновлені файли локалізації в папку SteamMods гри Gloomhaven
set "SRC_DIR=C:\Users\cakam\Documents\GitHub\GloomHavenUa"
set "DEST_DIR=C:\Users\cakam\AppData\LocalLow\FlamingFowlStudios\Gloomhaven\SteamMods\UkraineHaven"

echo [1/3] Копіювання файлів локалізації...
echo Джерело: %SRC_DIR%\LangPacks
echo Ціль:    %DEST_DIR%\LangPacks
echo.

if not exist "%DEST_DIR%\LangPacks" mkdir "%DEST_DIR%\LangPacks"

copy /Y "%SRC_DIR%\gloom.mod" "%DEST_DIR%\" > nul
copy /Y "%SRC_DIR%\thumbnail.png" "%DEST_DIR%\" > nul
xcopy /E /I /Y "%SRC_DIR%\LangPacks" "%DEST_DIR%\LangPacks" > nul

if %ERRORLEVEL% equ 0 (
    echo [OK] Файли успішно скопійовано!
) else (
    echo [ERROR] Помилка копіювання файлів.
    pause
    exit /b %ERRORLEVEL%
)
echo.

:: 2. Запитуємо параметри облікового запису та оновлення
echo [2/3] Введіть дані для входу в Steam:
set /p STEAM_USER="Введіть логін Steam: "

:: Створюємо тимчасовий VDF файл конфігурації для SteamCMD
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
echo [3/3] Запуск завантаження в Steam Workshop...
echo (Вам потрібно буде ввести ваш пароль Steam і, якщо увімкнено, код Steam Guard)
echo.

"%SRC_DIR%\steamcmd\steamcmd.exe" +login "%STEAM_USER%" +workshop_build_item "%VDF_FILE%" +quit

:: Видаляємо тимчасовий VDF файл задля чистоти
if exist "%VDF_FILE%" del "%VDF_FILE%"

echo.
echo ===================================================
echo Процес завершено.
echo ===================================================
pause
