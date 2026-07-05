# PersonaWeaver 前端 Electron 打包脚本（自包含配置版）
# 用法（在 charpick 环境的 PowerShell 里）：
#   powershell -ExecutionPolicy Bypass -File build_frontend.ps1
#
# 本脚本做三件事：
#   1) 用【本目录的 .env.local】作为构建配置，去前端源码目录跑 vite build
#   2) 把构建产物 dist 同步到本目录
#   3) 打成绿色免安装 exe（release\win-unpacked\PersonaWeaver.exe）
#      —— 并手动重建 app.asar，绕过 electron-builder 的 dist 缓存 bug
#
# 【重要】前端配置是“构建时”注入编译进 exe 的：
#   - 改配置 = 改本目录 .env.local，然后重跑本脚本（exe 成品旁边放配置文件无效）
#   - 首次使用：把 .env.local.example 复制为 .env.local 并填入真实值
#
# 关键坑（脚本已处理）：
#   - ELECTRON_RUN_AS_NODE 必须清除，否则 Electron 退化为纯 Node、白屏/崩溃
#   - electron 走 npmmirror 镜像，否则从 github 下载超时
#   - 缓存放非 C 盘，避免 C 盘膨胀
#   - electron-builder 有 dist 缓存 bug → 用 @electron/asar 手动重建 asar 修正

param(
    [string]$FrontendSrc = "E:\codes\CharPick-frontend",
    [string]$Node = "D:\系统环境\node.exe",
    [string]$Npm = "D:\系统环境\node_modules\npm\bin\npm-cli.js"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

Remove-Item Env:\ELECTRON_RUN_AS_NODE -ErrorAction SilentlyContinue
$env:ELECTRON_MIRROR = "https://npmmirror.com/mirrors/electron/"
$env:ELECTRON_BUILDER_BINARIES_MIRROR = "https://npmmirror.com/mirrors/electron-builder-binaries/"
$env:ELECTRON_CACHE = "E:\npm-cache\electron-cache"

Push-Location $here
try {
    # 0) 检查配置
    if (-not (Test-Path ".env.local")) {
        Write-Host "缺少 .env.local，请先复制 .env.local.example 为 .env.local 并填入真实值。" -ForegroundColor Red
        exit 1
    }

    # 1) 用本目录 .env.local 作为构建配置，去前端源码构建
    if (-not (Test-Path (Join-Path $FrontendSrc "package.json"))) {
        Write-Host "找不到前端源码：$FrontendSrc" -ForegroundColor Red
        exit 1
    }
    Copy-Item ".env.local" (Join-Path $FrontendSrc ".env.local") -Force
    Push-Location $FrontendSrc
    if (-not (Test-Path "node_modules")) {
        & $Node $Npm install --registry=https://registry.npmmirror.com --cache E:\npm-cache
    }
    & "node_modules\.bin\vite.cmd" build --base=./
    Pop-Location

    # 2) 同步 dist 到本目录
    Remove-Item "dist" -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item (Join-Path $FrontendSrc "dist") "dist" -Recurse -Force

    # 3) 依赖 + electron-builder 打包
    if (-not (Test-Path "node_modules\electron\dist\electron.exe")) {
        & $Node $Npm install --registry=https://registry.npmmirror.com --cache E:\npm-cache
    }
    Remove-Item "release" -Recurse -Force -ErrorAction SilentlyContinue
    & $Node "node_modules\electron-builder\out\cli\cli.js" --win dir

    # 3b) 手动重建 app.asar（修 electron-builder dist 缓存 bug）
    $stage = "_app_stage"
    Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force $stage | Out-Null
    Copy-Item "electron-main.js" $stage -Force
    Copy-Item "package.json" $stage -Force
    Copy-Item "dist" (Join-Path $stage "dist") -Recurse -Force
    $asarJs = "require('@electron/asar').createPackage('_app_stage','release/win-unpacked/resources/app.asar').then(function(){console.log('asar rebuilt')})"
    & $Node -e $asarJs
    Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue

    # 4) 附带使用说明
    if (Test-Path "assets\使用说明.txt") {
        Copy-Item "assets\使用说明.txt" "release\win-unpacked\使用说明.txt" -Force
    }

    Write-Host "`n完成，产物：release\win-unpacked\PersonaWeaver.exe" -ForegroundColor Green
}
finally {
    Pop-Location
}
