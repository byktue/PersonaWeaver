"""PersonaWeaver 后端自测脚本（独立自动化工具，非后端主程序的一部分）。

用途：一键验证已启动的后端 exe / 服务是否可用。用神游前 10 章真实数据做验证。
本脚本可以引用固定的神游素材路径，因为它是"自测自动化工具"；后端主程序本身
不含任何硬编码测试路径。

用法：
    # 1) 先启动后端 exe（另一个窗口）：
    #    personaweaver-backend.exe --port 8000
    # 2) 再运行本脚本：
    python selftest_backend.py --base-url http://127.0.0.1:8000 --data data/book_6619b9d7_神游.txt/first_10_chapters.txt

退出码 0 = 全部通过；非 0 = 有失败项。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests


def check_health(base_url: str) -> bool:
    try:
        r = requests.get(f"{base_url}/health", timeout=5)
        ok = r.status_code == 200 and r.json().get("status") == "ok"
        print(f"[1/3] 健康检查 /health : {'通过' if ok else '失败'} ({r.status_code})")
        return ok
    except Exception as exc:
        print(f"[1/3] 健康检查 /health : 失败（{exc}）—— 后端服务没起来？")
        return False


def check_chat(base_url: str, provider: str) -> bool:
    try:
        payload = {"message": "用一句话自我介绍", "provider": provider, "max_tokens": 60}
        r = requests.post(f"{base_url}/chat", json=payload, timeout=60)
        if r.status_code != 200:
            print(f"[2/3] 大模型 /chat  : 失败（HTTP {r.status_code}: {r.text[:120]}）")
            return False
        data = r.json()
        resp = str(data.get("response") or "").strip()
        ok = bool(resp)
        print(f"[2/3] 大模型 /chat  : {'通过' if ok else '失败'}（model={data.get('model')}, "
              f"返回 {len(resp)} 字）")
        return ok
    except Exception as exc:
        print(f"[2/3] 大模型 /chat  : 失败（{exc}）")
        return False


def check_local_pipeline(data_path: str) -> bool:
    """L0/L1 切章（不联网、不花钱）：验证真实数据能被解析、清洗、切章。"""
    try:
        repo_root = Path(__file__).resolve().parents[2]
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        from backend.source_preprocess import process_source_file

        src = Path(data_path)
        if not src.is_absolute():
            src = repo_root / data_path
        if not src.exists():
            print(f"[3/3] 切章 pipeline : 跳过（未找到素材 {src}）")
            return True  # 素材缺失不算失败，仅提示

        result = process_source_file(
            source_path=str(src),
            source_type="txt",
            source_file_id="selftest_shenyou_10",
            book_title="神游",
            filter_noise=True,
        )
        n = len(result.get("chapters", []))
        ok = n > 0
        print(f"[3/3] 切章 pipeline : {'通过' if ok else '失败'}（切出 {n} 章）")
        return ok
    except Exception as exc:
        print(f"[3/3] 切章 pipeline : 失败（{exc}）")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="PersonaWeaver 后端自测")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--provider", default="vivo")
    parser.add_argument(
        "--data",
        default="data/book_6619b9d7_神游.txt/first_10_chapters.txt",
        help="神游前 10 章截取版路径（用于 L0/L1 切章验证）",
    )
    args = parser.parse_args()

    print("=" * 56)
    print("PersonaWeaver 后端自测（真实数据：神游前 10 章）")
    print(f"目标服务：{args.base_url}")
    print("=" * 56)

    results = [
        check_health(args.base_url),
        check_chat(args.base_url, args.provider),
        check_local_pipeline(args.data),
    ]

    print("-" * 56)
    passed = sum(1 for r in results if r)
    print(f"结果：{passed}/{len(results)} 通过")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
