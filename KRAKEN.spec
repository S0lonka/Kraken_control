# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app\\KRAKEN.py'],
    pathex=[
    'C:\\Users\\Solonka\\Documents\\GitHub\\Kraken_control\\.venv\\Lib\\site-packages',  # Путь к qasync
    'app',  # Путь к папке app
    'C:\\Users\\Solonka\\Documents\\GitHub\\Kraken_control\\app\\interfaces\\utils\\resource'
    ],
    binaries=[],
    datas=[
        ('c:\\Users\\Solonka\\Documents\\GitHub\\Kraken_control\\resources\\img\\imgReadme', 'resources\\img\\imgReadme'),
    ],
    hiddenimports=['interfaces'],
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
    name='KRAKEN',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\icon.ico'],
)
