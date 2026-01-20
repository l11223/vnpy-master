# -*- mode: python ; coding: utf-8 -*-
# VNPY Mac版 PyInstaller打包配置

block_cipher = None

a = Analysis(
    ['启动量化系统.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('vnpy', 'vnpy'),
    ],
    hiddenimports=[
        'vnpy.trader',
        'vnpy.trader.platform_utils',
        'vnpy.trader.multiprocess_manager',
        'vnpy.trader.enhanced_cta_template',
        'vnpy.trader.history_manager',
        'vnpy.trader.data_filter',
        'vnpy.trader.optimization_metrics',
        'vnpy.trader.enhanced_risk_manager',
        'vnpy.trader.status_monitor',
        'vnpy.trader.gateway_mac_adapter',
        'loguru',
        'tzlocal',
        'talib',
        'PySide6',
        'qdarkstyle',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VNPY-Optimized',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Mac GUI模式，不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='VNPY.app',
    icon=None,  # 如果有图标，改为 'vnpy.icns'
    bundle_identifier='com.vnpy.optimized',
)
