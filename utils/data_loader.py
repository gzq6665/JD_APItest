from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json_data(file_path: str | Path) -> dict[str, Any]:
    """读取 JSON 测试数据文件。"""

    path = Path(file_path)
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    if not isinstance(payload, dict):
        raise ValueError(f"测试数据文件必须是 JSON 对象：{path}")
    return payload


def load_test_cases(file_path: str | Path) -> list[dict[str, Any]]:
    """读取参数化测试数据，要求 JSON 中包含 cases 列表。"""

    payload = load_json_data(file_path)
    cases = payload.get("cases", [])
    if not isinstance(cases, list):
        raise ValueError(f"测试数据中的 cases 必须是列表：{file_path}")
    return cases


def build_case_ids(cases: list[dict[str, Any]]) -> list[str]:
    """生成 pytest 参数化显示名称。"""

    ids: list[str] = []
    for index, case in enumerate(cases, start=1):
        case_id = case.get("case_id") or case.get("title") or f"case_{index}"
        ids.append(str(case_id))
    return ids
