# 📁 Folder Creator

Aplicación de escritorio en Python + Tkinter para crear múltiples carpetas de forma manual o automática mediante un CSV.

---

## 🚀 Requisitos

- **Python 3.8+** → https://python.org
- **tkinter** (incluido en Windows y macOS; en Linux: `sudo apt install python3-tk`)

---

## ⚙️ Instalación para desarrollo

### 1. Crear entorno virtual

**Windows:**
```bat
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Ejecutar la app
```bash
python app.py
```

---

## 📦 Generar ejecutable (.exe / binario)

Con PyInstaller puedes generar un archivo que **no necesita Python instalado** y se puede compartir directamente.

### Windows → genera `dist\FolderCreator.exe`
```bat
build.bat
```

### macOS / Linux → genera `dist/FolderCreator`
```bash
chmod +x build.sh && ./build.sh
```

El script activa el entorno virtual, instala PyInstaller y construye el ejecutable en `dist/`.

**¿Qué compartir?** Solo el archivo `dist/FolderCreator.exe`. Sin Python, sin instalación — doble clic y listo.

---

## 🗂 Funcionalidades

| Función | Descripción |
|---|---|
| **Lista manual** | Agrega/elimina nombres con `+ Agregar fila` |
| **Directorio destino** | Elige la ruta donde se crearán las carpetas |
| **Importar CSV** | Carga un `.csv` con nombres separados por comas |
| **Crear carpetas** | Crea todas; reporta creadas, omitidas y errores |

---

## 📄 Formato del CSV

```
ventas,marketing,rrhh,finanzas
```

---

## 🗃 Estructura

```
folder_creator/
├── app.py
├── icon.ico
├── folder_creator.spec
├── build.bat / build.sh
├── setup.bat / setup.sh
├── ejemplo.csv
├── requirements.txt
├── README.md
└── .vscode/
```

