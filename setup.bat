@echo off
setlocal

where uv >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [OK] uv is already installed.
) else (
    echo [INFO] uv is not installed.
    echo [INFO] Installing uv...

    powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"

    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install uv.
        echo Please install uv manually.
        exit /b 1
    )

    set "PATH=%USERPROFILE%\.local\bin;%PATH%"

    where uv >nul 2>&1

    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] uv was installed but could not be found in PATH.
        echo Please restart this terminal and run setup.bat again.
        exit /b 1
    )

    echo [OK] uv installed successfully.
)

echo [INFO] Installing Python 3.14

uv python install 3.14 --default
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Python 3.14.
    exit /b 1
)

echo [INFO] Installing project dependencies...

uv sync

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Dependency installation failed.
    exit /b 1
)

echo [OK] Dependencies installed.

echo [INFO] Setting up database tables...

uv run alembic upgrade head
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Database setup failed.
    exit /b 1
)

echo [OK] Database setup completed.
