"""PersonaWeaver 后端服务型 exe 启动器。

设计要点（对应《后端交付与数据清洗共识》第二章）：
- 服务型：常驻监听 127.0.0.1 + 可配置端口，前端通过 HTTP 调用。
- 敏感配置不打进 exe：运行时从 exe 同目录的 .env 读取（Supabase/OSS/LLM key）。
- 运行数据落在 exe 同目录（local_cache/ output/），整包放哪盘就写哪盘，不碰 C 盘。
- 可选启动 token：设置环境变量 BACKEND_TOKEN 后，健康检查外的调用需带该 token。

打包（onedir 模式，产物为一个文件夹，便于绿色免安装分发）：
    见 build_backend.ps1
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def _app_dir() -> Path:
    """exe 所在目录（frozen）或脚本所在目录（源码运行）。运行数据与 .env 都以此为基准。"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _load_env_from(app_dir: Path) -> str:
    """把 exe 同目录 .env 预加载进 os.environ，先于 backend.main 导入，确保其读到 key。"""
    env_path = app_dir / ".env"
    if not env_path.exists():
        return f"(未找到 {env_path}，仅使用系统环境变量)"
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        # 先加载者优先：这里最先写入，backend 内部的 _load_dotenv_simple 不会覆盖。
        os.environ.setdefault(key, value)
    return f"(已加载 {env_path})"


def main() -> None:
    parser = argparse.ArgumentParser(description="PersonaWeaver 后端服务型 exe")
    parser.add_argument("--host", default=os.getenv("BACKEND_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("BACKEND_PORT", "8000")))
    args = parser.parse_args()

    app_dir = _app_dir()
    # 让 backend 内部所有以 CWD 为基准的相对写入（local_cache/、output/）落在包目录内。
    os.chdir(app_dir)
    env_status = _load_env_from(app_dir)

    # 源码运行时需要能 import backend 包；frozen 下 backend 已打进 exe。
    if not getattr(sys, "frozen", False):
        repo_root = Path(__file__).resolve().parents[2]
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))

    import uvicorn
    from backend.main import app

    print("=" * 60)
    print("PersonaWeaver 后端服务启动")
    print(f"  程序目录 : {app_dir}")
    print(f"  .env     : {env_status}")
    print(f"  监听地址 : http://{args.host}:{args.port}")
    print(f"  健康检查 : http://{args.host}:{args.port}/health")
    print("  停止服务 : 关闭本窗口或 Ctrl+C")
    print("=" * 60)

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
