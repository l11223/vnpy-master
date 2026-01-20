# -*- mode: python ; coding: utf-8 -*-
"""
VNPY Mac版 PyInstaller打包配置
使用 --onefile 模式（最简单可靠）

关键：在 macOS 上，--onefile + --windowed 会自动创建正确的 .app 结构
"""

import sys
import os

block_cipher = None

# 分析阶段
a = Analysis(
    ['vnpy_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('vnpy', 'vnpy'),
    ],
    hiddenimports=[
        'vnpy',
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
        'vnpy.trader.multiprocess_backtester',
        'vnpy.trader.optimization_visualization',
        'vnpy.alpha',
        'vnpy.alpha.strategy',
        'vnpy.alpha.strategy.template',
        'vnpy.alpha.strategy.strategies',
        'vnpy.event',
        'vnpy.trader.engine',
        'vnpy.trader.ui',
        'vnpy.trader.ui.mainwindow',
        'vnpy.trader.ui.widget',
        'loguru',
        'tzlocal',
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
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

# --onefile 模式：所有内容打包成单个可执行文件
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
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI模式，不显示终端
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS .app 包
# 在 --onefile 模式下，BUNDLE 直接接收 EXE
app = BUNDLE(
    exe,
    name='VNPY-Optimized.app',
    icon=None,
    bundle_identifier='com.vnpy.optimized',
    info_plist={
        'CFBundleName': 'VNPY',
        'CFBundleDisplayName': 'VNPY量化交易系统',
        'CFBundleExecutable': 'VNPY-Optimized',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'CFBundlePackageType': 'APPL',
        'LSMinimumSystemVersion': '10.15',
        'NSHighResolutionCapable': True,
        'LSUIElement': False,
        'NSRequiresAquaSystemAppearance': False,
    },
)
