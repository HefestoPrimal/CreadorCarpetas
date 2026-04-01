@echo off
echo ===================================
echo   Folder Creator - Setup
echo ===================================
echo.

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado. Instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado.

:: Crear entorno virtual
if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
    echo [OK] Entorno virtual creado en .venv\
) else (
    echo [OK] Entorno virtual ya existe.
)

echo.
echo Para activar el entorno virtual ejecuta:
echo   .venv\Scripts\activate
echo.
echo Para iniciar la aplicacion:
echo   python app.py
echo.
pause
