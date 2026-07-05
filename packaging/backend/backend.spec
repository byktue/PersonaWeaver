# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec：把 PersonaWeaver 后端打成服务型 exe（onedir，绿色免安装）。

产物：dist/personaweaver-backend/  （整个文件夹分发，放任意盘符）
不打进 exe 的：.env（敏感配置，运行时从 exe 同目录读）。
打进 exe 的：backend/config.json（prompts 与非敏感 provider 元信息）。
"""
import glob
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

datas = []
binaries = []
hiddenimports = []

# conda 环境的 C 扩展 DLL 不在标准位置，需显式打包，否则 frozen exe 导入
# _ssl / _ctypes / pyexpat 等失败（pyexpat 缺失会连带 oss2 导入失败）。
_conda_lib_bin = os.path.join(os.path.dirname(os.__file__), "..", "Library", "bin")
for _dll in ("libssl-3-x64.dll", "libcrypto-3-x64.dll", "ffi-*.dll", "libffi*.dll",
             "libexpat*.dll", "expat*.dll"):
    for _hit in glob.glob(os.path.join(_conda_lib_bin, _dll)):
        binaries.append((_hit, "."))

# 需要完整收集的第三方包（含数据文件 / 动态子模块）——这些缺失不致命，容错。
for pkg in ("supabase", "postgrest", "storage3", "supabase_auth", "supabase_functions",
            "realtime", "gotrue", "langextract", "google", "psycopg2", "aliyun"):
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

# OSS 上传关键依赖：不容错，缺了直接让构建报错，避免打出"运行时才崩"的 exe。
# pycryptodome(Crypto) 含 .pyd C 扩展，必须完整收集其 binaries。
for pkg in ("oss2", "crcmod", "Crypto", "aliyunsdkcore", "aliyunsdkkms"):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

# 显式声明动态/条件导入的子模块，确保静态分析不漏。
hiddenimports += collect_submodules("oss2")
hiddenimports += collect_submodules("Crypto")
hiddenimports += ["crcmod", "crcmod._crcfunext", "aliyunsdkcore", "aliyunsdkkms"]

hiddenimports += collect_submodules("uvicorn")
hiddenimports += ["backend", "backend.main", "backend.long",
                  "backend.remote_persistence", "backend.workflow_runner"]

# 把后端运行期需要的 config.json 打进 bundle（backend 包内相对定位）
datas += [("../../backend/config.json", "backend")]

block_cipher = None

a = Analysis(
    ["backend_server.py"],
    pathex=["../.."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "pandas.tests"],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="personaweaver-backend",
    console=True,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="personaweaver-backend",
)
