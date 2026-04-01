#!/usr/bin/env bash
set -e

echo "==================================="
echo "  Folder Creator – Setup"
echo "==================================="
echo ""

# Verificar Python
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python3 no encontrado. Instala Python 3.8+ desde https://python.org"
    exit 1
fi

echo "[OK] $(python3 --version) encontrado."

# Verificar tkinter
python3 -c "import tkinter" 2>/dev/null || {
    echo "[AVISO] tkinter no está disponible."
    echo "  Ubuntu/Debian:  sudo apt install python3-tk"
    echo "  Fedora:         sudo dnf install python3-tkinter"
    echo "  macOS (brew):   brew install python-tk"
    exit 1
}
echo "[OK] tkinter disponible."

# Crear entorno virtual
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
    echo "[OK] Entorno virtual creado en .venv/"
else
    echo "[OK] Entorno virtual ya existe."
fi

echo ""
echo "Para activar el entorno virtual:"
echo "  source .venv/bin/activate"
echo ""
echo "Para iniciar la aplicación:"
echo "  python app.py"
echo ""
