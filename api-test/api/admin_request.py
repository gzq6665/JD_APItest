from __future__ import annotations

from requests import Response

from utils.client import ApiClient


class AdminRequestApi:
    """后台系统请求脚本。"""

    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def get_login_image_code(self) -> Response:
        return self.client.request("GET", "/common/public/verifycode/0.4516361871404062")

    def login(self, *, username: str, password: str, valicode: str) -> Response:
        return self.client.request(
            "POST",
            "/system/public/verifyLogin",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "username": username,
                "password": password,
                "valicode": valicode,
            },
        )

    def search_amount_apply_list(self, *, member_name: str, category_id: str) -> Response:
        return self.client.request(
            "POST",
            "/loan/amount/applyData",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "member_name": member_name,
                "category_id": category_id,
            },
        )

    def open_amount_verify_page(self, *, editid: str) -> Response:
        return self.client.request("POST", f"/loan/amount/verify&editid={editid}")

    def get_verify_image_code(self) -> Response:
        return self.client.request("GET", "/common/public/verifycode/0.5818739207276852")

    def submit_amount_verify(
        self,
        *,
        editid: str,
        member_id: str,
        amount: str,
        add_ip: str,
        category_id: str,
        remark: str,
        record_id: str,
        member_name: str,
        verify_type: str,
        add_time: str,
        income_amount: str,
        status: str,
        verify_remark: str,
        valicode: str,
    ) -> Response:
        return self.client.request(
            "POST",
            "/loan/amount/verifysubmit",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "editid": editid,
                "member_id": member_id,
                "amount": amount,
                "add_ip": add_ip,
                "category_id": category_id,
                "remark": remark,
                "id": record_id,
                "member_name": member_name,
                "type": verify_type,
                "add_time": add_time,
                "income_amount": income_amount,
                "status": status,
                "verify_remark": verify_remark,
                "valicode": valicode,
            },
        )

    def get_amount_apply_log(self, *, member_name: str) -> Response:
        return self.client.request(
            "POST",
            "/loan/amount/applyLogData",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"member_name": member_name},
        )
