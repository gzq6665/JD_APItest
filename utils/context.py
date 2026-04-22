from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TestContext:
    """保存跨接口流转的上下文变量。"""

    __test__ = False

    phone: str = ""
    password: str = "a123456"
    realname: str = ""
    card_id: str = ""
    editid: str = ""
    member_id: str = ""
    amount: str = ""
    remark: str = ""
    record_id: str = ""
