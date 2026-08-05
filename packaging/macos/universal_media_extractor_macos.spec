# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Universal Media Extractor macOS production foundation."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules


project_root = Path(SPECPATH).parents[1]
src_dir = project_root / "src"
static_dir = src_dir / "universal_media_extractor" / "static"

hiddenimports = []
hiddenimports += collect_submodules("uvicorn")
hiddenimports += collect_submodules("webview")
hiddenimports += [
    "httptools.parser.parser",
    "uvloop.loop",
    "watchfiles._rust_notify",
]

datas = [
    (str(static_dir), "universal_media_extractor/static"),
]


a = Analysis(
    [str(project_root / "scripts" / "run_desktop.py")],
    pathex=[str(src_dir), str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name="Universal Media Extractor",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Universal Media Extractor",
)
app = BUNDLE(
    coll,
    name="Universal Media Extractor.app",
    icon=None,
    bundle_identifier="com.shteinyr.universal-media-extractor",
    info_plist={
        "CFBundleDisplayName": "Universal Media Extractor",
        "CFBundleName": "Universal Media Extractor",
        "CFBundleShortVersionString": "0.1.0",
        "CFBundleVersion": "1",
        "LSMinimumSystemVersion": "12.0",
        "NSHighResolutionCapable": True,
        "NSAppTransportSecurity": {
            "NSAllowsArbitraryLoads": True,
            "NSAllowsLocalNetworking": True,
        },
    },
)
