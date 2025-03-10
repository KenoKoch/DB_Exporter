# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\kkoch\\OneDrive - BorgWarner\\Desktop\\DB_Exporter\\DB_Exporter-Allgemein\\venv\\Lib\\site-packages\\snap7\\lib\\snap7.dll', '.'), ('Daten.db', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\kkoch\\OneDrive - BorgWarner\\Desktop\\DB_Exporter\\DB_Exporter-Allgemein\\Icon.ico'],
)
