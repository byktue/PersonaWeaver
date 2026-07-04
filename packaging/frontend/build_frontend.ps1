# PersonaWeaver 前端 Electron 打包脚本
# 用法（在 charpick 环境的 PowerShell 里）：
#   powershell -ExecutionPolicy Bypass -File build_frontend.ps1
#
# 前置：前端源码已 npm install 并 vite build 出 dist/。本脚本会：
#   1) 从前端工程复制最新 dist/ 到本目录
#   2) electron-builder 打成绿色免安装 exe（release/win-unpacked/PersonaWeaver.exe）
#
# 关键坑（务必按此设置，否则打包/启动失败）：
#   - ELECTRON_RUN_AS_NODE 必须清除：否则 Electron 以纯 Node 运行，require('electron').app 为 undefined
#   - 国内网络需设 ELECTRON_MIRROR / ELECTRON_BUILDER_BINARIES_MIRROR 指向 npmmirror，
#     否则 electron-builder 从 github 下载 electron zip 会超时
#   - npm 缓存与 electron 缓存放非 C 盘（E:\npm-cache），避免 C 盘膨胀

param(
    [string]$FrontendSrc = "E:\codes\CharPick-frontend",
    [string]$Node = "D:\系统环境\node.exe"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

# 清除会导致 Electron 退化为 Node 的环境变量
Remove-Item Env:\ELECTRON_RUN_AS_NODE -ErrorAction SilentlyContinue

# 国内镜像 + 缓存挪到 E 盘
$env:ELECTRON_MIRROR = "https://npmmirror.com/mirrors/electron/"
$env:ELECTRON_BUILDER_BINARIES_MIRROR = "https://npmmirror.com/mirrors/electron-builder-binaries/"
$env:ELECTRON_CACHE = "E:\npm-cache\electron-cache"

Push-Location $here
try {
    # 1) 同步最新前端构建产物
    if (-not (Test-Path (Join-Path $FrontendSrc "dist\index.html"))) {
        Write-Host "前端未构建，请先在 $FrontendSrc 执行 vite build" -ForegroundColor Red
        exit 1
    }
    Remove-Item "dist" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item (Join-Path $FrontendSrc "dist") "dist" -Recurse -Force

    # 2) 依赖（首次需要）
    if (-not (Test-Path "node_modules\electron\dist\electron.exe")) {
        & $Node "D:\系统环境\node_modules\npm\bin\npm-cli.js" install --registry=https://registry.npmmirror.com --cache E:\npm-cache
    }

    # 3) electron-builder 绿色免安装
    & $Node "node_modules\electron-builder\out\cli\cli.js" --win dir

    Write-Host "`n产物：release\win-unpacked\PersonaWeaver.exe" -ForegroundColor Green
}
finally {
    Pop-Location
}
