# -*- mode: python ; coding: utf-8 -*-
# Archivo de configuración para PyInstaller
# Ejecutar con: pyinstaller folder_creator.spec

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'),   # incluye el ícono dentro del ejecutable
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'pandas', 'matplotlib', 'PIL'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FolderCreator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # sin ventana de terminal negra
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',        # ícono del .exe en el explorador
)
