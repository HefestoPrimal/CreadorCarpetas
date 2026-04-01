# 📁 Folder Creator

Aplicación de escritorio en Python + Tkinter para crear múltiples carpetas de forma manual o automática mediante un CSV.

---

## 🚀 Requisitos

- **Python 3.8+** → https://python.org
- **tkinter** (incluido en Windows y macOS; en Linux: `sudo apt install python3-tk`)

---

## ⚙️ Instalación

### Windows
```bat
setup.bat
```

### macOS / Linux
```bash
chmod +x setup.sh
./setup.sh
```

Esto verifica Python, tkinter y crea el entorno virtual en `.venv/`.

---

## ▶️ Uso

### 1. Activar el entorno virtual

**Windows:**
```bat
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 2. Ejecutar la app
```bash
python app.py
```

---

## 🗂 Funcionalidades

| Función | Descripción |
|---|---|
| **Lista manual** | Agrega/elimina nombres de carpeta con el botón `+ Agregar fila` |
| **Directorio destino** | Elige la ruta donde se crearán las carpetas (botón *Examinar*) |
| **Importar CSV** | Carga un `.csv` con nombres separados por comas y los importa a la lista |
| **Crear carpetas** | Crea todas las carpetas listadas; reporta creadas, omitidas y errores |

---

## 📄 Formato del CSV

El CSV puede tener los nombres en una sola fila separados por comas, o en múltiples filas:

```
ventas,marketing,rrhh,finanzas
```

También válido:
```
ventas
marketing
rrhh
```

Se incluye un archivo `ejemplo.csv` para probar.

---

## 🗃 Estructura del proyecto

```
folder_creator/
├── app.py          ← Aplicación principal
├── ejemplo.csv     ← CSV de ejemplo
├── requirements.txt
├── setup.bat       ← Setup Windows
├── setup.sh        ← Setup macOS/Linux
└── README.md
```

---

## 💡 Abriendo en VSCode

1. Abre la carpeta `folder_creator/` en VSCode
2. Selecciona el intérprete de Python: `.venv/Scripts/python` (Windows) o `.venv/bin/python` (macOS/Linux)
3. Ejecuta `app.py` con `F5` o la terminal integrada
