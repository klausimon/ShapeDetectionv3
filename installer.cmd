@echo off
echo Checking for Python 3.6+ installation...

:: Check if Python is accessible
python --version 2>nul
if %errorlevel% neq 0 (
    echo Error: Python not found in PATH.
    echo Please ensure Python 3.6 or newer is installed from:
    echo https://www.python.org/
    echo And verify it's added to your system PATH.
    pause
    exit /b 1
)

:: Verify Python version >= 3.6
echo Checking Python version...
python -c "import sys; sys.exit(0) if sys.version_info >= (3, 6) else sys.exit(1)"
if %errorlevel% neq 0 (
    echo Error: Python 3.6 or newer is required.
    echo Detected version: 
    python --version
    echo Please update your Python installation.
    pause
    exit /b 1
)

:: Check for pip
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip package manager not found.
    echo Consider installing pip or check Python installation.
    pause
    exit /b 1
)

:: Install packages
echo Installing packages (opencv-python, numpy, Pillow)...
python -m pip install --upgrade opencv-python numpy Pillow

:: Verify installation success
if %errorlevel% neq 0 (
    echo Error: Package installation failed.
    echo Try these solutions:
    echo 1. Run as Administrator
    echo 2. Check internet connection
    echo 3. Update pip: python -m pip install --upgrade pip
    pause
    exit /b 1
)

echo Successfully installed all packages!
pause