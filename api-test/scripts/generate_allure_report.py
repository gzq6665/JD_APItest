from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "report"
ALLURE_RESULTS_DIR = REPORT_DIR / "allure-results"
ALLURE_REPORT_DIR = REPORT_DIR / "allure-report"


def _reset_dir(directory: Path) -> None:
    """删除旧目录后重新创建，避免历史结果污染本次报告。"""

    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)


def _run_command(command: list[str]) -> None:
    """执行命令，任何一步失败都直接抛出异常。"""

    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def _resolve_allure_executable() -> str:
    """优先从 PATH 查找 allure，其次回退到项目同级目录下的 Windows 安装路径。"""

    allure_path = shutil.which("allure") or shutil.which("allure.bat")
    if allure_path:
        return allure_path

    parent_dir = PROJECT_ROOT.parent
    candidates = sorted(parent_dir.glob("allure-*/allure-*/bin/allure.bat"))
    if candidates:
        return str(candidates[-1])

    raise FileNotFoundError("未找到 allure 可执行文件，请先确认本机已安装 Allure CLI。")


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _reset_dir(ALLURE_RESULTS_DIR)
    allure_executable = _resolve_allure_executable()

    # 第一步：执行 pytest，并把原始结果输出到 allure-results。
    _run_command(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            f"--alluredir={ALLURE_RESULTS_DIR}",
        ]
    )

    # 第二步：根据结果目录生成可离线打开的 HTML 报告。
    _run_command(
        [
            allure_executable,
            "generate",
            str(ALLURE_RESULTS_DIR),
            "-c",
            "-o",
            str(ALLURE_REPORT_DIR),
        ]
    )

    print(f"Allure 原始结果目录: {ALLURE_RESULTS_DIR}")
    print(f"Allure 离线报告目录: {ALLURE_REPORT_DIR}")
    print("打开 report/allure-report/index.html 即可离线查看报告。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
