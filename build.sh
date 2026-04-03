#!/usr/bin/env bash
set -e

echo "==================================================="
echo "  Folder Creator – Build ejecutable"
echo "==================================================="
echo ""

# Verificar entorno virtual
if [ ! -f ".venv/bin/activate" ]; then
    echo "[ERROR] No se encontró el entorno virtual."
    echo "Ejecuta primero: python3 -m venv .venv"
    exit 1
fi

source .venv/bin/activate
echo "[OK] Entorno virtual activado."

# Instalar PyInstaller
echo ""
echo "Instalando PyInstaller..."
pip install pyinstaller --quiet
echo "[OK] PyInstaller listo."

# Limpiar builds anteriores
rm -rf dist build
echo "[OK] Carpetas anteriores limpiadas."

# Construir
echo ""
echo "Construyendo ejecutable..."
echo "(Esto puede tardar 30-60 segundos)"
echo ""
pyinstaller folder_creator.spec

# Resultado
if [ -f "dist/FolderCreator" ]; then
    echo ""
    echo "==================================================="
    echo "  BUILD EXITOSO"
    echo "  Archivo: dist/FolderCreator"
    echo "==================================================="
else
    echo "[ERROR] El build falló. Revisa los mensajes arriba."
    exit 1
fi
