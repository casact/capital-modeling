@echo off
setlocal

REM =============================================================
REM Optional argument: Python version for uv branch (default 3.13)
REM Usage: setup.bat [3.13]
REM =============================================================
set "PY_VER=%~1"
if "%PY_VER%"=="" set "PY_VER=3.13"

REM =============================================================
REM Configuration
REM =============================================================

REM Working directory for this project inside %TEMP%
set "WORK_DIR=%TEMP%\CMM"

REM Detect source repo:
REM - If we are inside a git repo: use that repo as source.
REM - Otherwise: clone from GitHub.
git rev-parse --show-toplevel >nul 2>&1
if errorlevel 1 (
    echo Not in a git repository, using GitHub as source.
    set "SOURCE_REPO=https://github.com/casact/capital-modeling"
) else (
    for /f "delims=" %%G in ('git rev-parse --show-toplevel') do set "SOURCE_REPO=%%G"
    echo Using local git repository as source: "%SOURCE_REPO%"
)

REM =============================================================
REM Prepare temporary working directory
REM =============================================================

if exist "%WORK_DIR%" (
    echo Removing existing work directory "%WORK_DIR%" ...
    rmdir /s /q "%WORK_DIR%"
)

echo Cloning "%SOURCE_REPO%" into "%WORK_DIR%" ...
git clone "%SOURCE_REPO%" "%WORK_DIR%"
if errorlevel 1 (
    echo Git clone failed. Aborting.
    goto :EOF
)

cd /d "%WORK_DIR%"

REM =============================================================
REM Detect uv
REM =============================================================
where uv >nul 2>&1
if not errorlevel 1 (
    set "USE_UV=1"
) else (
    set "USE_UV=0"
)

REM =============================================================
REM Virtual environment + deps
REM =============================================================

if "%USE_UV%"=="1" (
    echo.
    echo uv detected. Using uv with Python %PY_VER% ...

    REM Pin project Python version
    uv python pin %PY_VER%
    if errorlevel 1 (
        echo uv python pin %PY_VER% failed. Aborting.
        goto :EOF
    )

    REM Create venv named "venv" using pinned / requested Python
    uv venv venv --python %PY_VER%
    if errorlevel 1 (
        echo uv venv --python %PY_VER% failed. Aborting.
        goto :EOF
    )

    call "venv\Scripts\activate.bat"

    echo Installing dependencies with uv pip ...
    uv pip install -r requirements.txt
    if errorlevel 1 (
        echo uv pip install failed. Aborting.
        goto :EOF
    )
) else (
    echo.
    echo uv not found. Falling back to python -m venv and pip ...
    if not exist "venv" (
        echo Creating virtual environment in "%WORK_DIR%\venv" ...
        python -m venv venv
        if errorlevel 1 (
            echo python -m venv failed. Aborting.
            goto :EOF
        )
    )

    call "venv\Scripts\activate.bat"

    echo Upgrading pip ...
    python -m pip install --upgrade pip

    echo Installing dependencies from requirements.txt ...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo pip install failed. Aborting.
        goto :EOF
    )
)

REM =============================================================
REM Project: Full Rebuild
REM =============================================================

echo.
echo Rebuilding HTML book with Quarto...
echo.

where quarto >nul 2>&1
if errorlevel 1 (
    echo.
    echo Quarto is not installed or not on PATH.
    echo Please install Quarto from https://quarto.org/docs/get-started/ before running this script.
    echo Aborting.
    goto :EOF
)

cd source
quarto render --to html

if errorlevel 1 (
    echo Quarto render failed. Aborting.
    goto :EOF
)

echo Quarto render successful, HTML book built.

REM =============================================================
REM Serve built site from docs and open in browser
REM =============================================================

cd /d "%WORK_DIR%\docs"

if not exist "index.html" (
    echo Warning: index.html not found in %WORK_DIR%\docs
) else (
    echo Output: %WORK_DIR%\docs
)

echo Starting web server on http://localhost:9955 ...
start "" python -m http.server 9955

REM Give the server a brief moment to start (optional but nice)
ping 127.0.0.1 -n 2 >nul

echo Opening index page in default browser...
start "" "http://localhost:9955/index.html"

echo.
echo Press Ctrl+C in the server window to stop the HTTP server.
echo.

endlocal
