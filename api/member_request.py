from __future__ import annotations

from requests import Response

from utils.client import ApiClient


class MemberRequestApi:
    """前台系统请求脚本。"""

    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def get_register_image_code(self) -> Response:
        return self.client.request("GET", "/common/public/verifycode1/0.24294740752448873")

    def send_sms(self, *, phone: str, img_verify_code: str, sms_type: str) -> Response:
        return self.client.request(
            "POST",
            "/member/public/sendSms",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "phone": phone,
                "imgVerifyCode": img_verify_code,
                "type": sms_type,
            },
        )

    def register(
        self,
        *,
        phone: str,
        verify_code: str,
        phone_code: str,
        password: str,
        dy_server: str,
    ) -> Response:
        return self.client.request(
            "POST",
            "/member/public/reg",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "phone": phone,
                "verifycode": verify_code,
                "phone_code": phone_code,
                "password": password,
                "dy_server": dy_server,
            },
        )

    def login(self, *, phone: str, password: str) -> Response:
        return self.client.request(
            "POST",
            "/member/public/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "keywords": phone,
                "password": password,
            },
        )

    def is_login(self) -> Response:
        return self.client.request("POST", "/member/public/islogin")

    def approve_realname(self, *, realname: str, card_id: str) -> Response:
        return self.client.request(
            "POST",
            "/member/realname/approverealname",
            headers={"Content-Type": "multipart/form-data"},
            multipart={
                "realname": realname,
                "card_id": card_id,
            },
        )

    def get_approve_info(self) -> Response:
        return self.client.request("POST", "/member/member/getapprove")

    def open_account(self) -> Response:
        return self.client.request("POST", "/trust/trust/register")

    def switch_account(self, *, user_role: int) -> Response:
        return self.client.request("GET", "/member/member/center", params={"user_role": user_role})

    def open_amount_page(self) -> Response:
        return self.client.request("GET", "/loan/amount/index")

    def get_amount_image_code(self) -> Response:
        return self.client.request("GET", "/common/public/verifycode/0.5067664511396726")

    def apply_amount(
        self,
        *,
        amount_type: str,
        amount_account: str,
        remark: str,
        verify_code: str,
    ) -> Response:
        return self.client.request(
            "POST",
            "/loan/amountapply/apply",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "amount_type": amount_type,
                "amount_account": amount_account,
                "remark": remark,
                "verifycode": verify_code,
            },
        )
