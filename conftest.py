from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from api.admin_request import AdminRequestApi
from api.member_request import MemberRequestApi
from utils.client import ApiClient
from utils.context import TestContext
from utils.data_factory import generate_random_chinese_name, generate_random_id_card, generate_random_phone
from utils.data_loader import load_test_cases
from utils.settings import Settings, get_settings


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def _first_case(file_path: Path) -> dict[str, Any]:
    cases = load_test_cases(file_path)
    if not cases:
        raise ValueError(f"测试数据为空：{file_path}")
    return cases[0]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture
def test_context() -> TestContext:
    """前置：生成当前用例所需的动态上下文。后置：yield 结束后自动释放。"""

    context = TestContext(
        phone=generate_random_phone(),
        password="a123456",
    )
    yield context


@pytest.fixture
def member_api(settings: Settings):
    """前置：创建前台请求会话。后置：关闭会话。"""

    client = ApiClient(settings.base_url, timeout=settings.timeout, verify=settings.verify_ssl)
    api = MemberRequestApi(client)
    yield api
    client.close()


@pytest.fixture
def admin_api(settings: Settings):
    """前置：创建后台请求会话。后置：关闭会话。"""

    client = ApiClient(settings.admin_base_url, timeout=settings.timeout, verify=settings.verify_ssl)
    api = AdminRequestApi(client)
    yield api
    client.close()


@pytest.fixture
def register_image_code_done(member_api: MemberRequestApi):
    return member_api.get_register_image_code()


@pytest.fixture
def send_sms_done(register_image_code_done, member_api: MemberRequestApi, test_context: TestContext):
    case_data = _first_case(DATA_DIR / "test_02_send_sms.json")
    return member_api.send_sms(
        phone=test_context.phone,
        img_verify_code=case_data["request"]["img_verify_code"],
        sms_type=case_data["request"]["type"],
    )


@pytest.fixture
def register_done(send_sms_done, member_api: MemberRequestApi, test_context: TestContext):
    case_data = _first_case(DATA_DIR / "test_03_register.json")
    return member_api.register(
        phone=test_context.phone,
        verify_code=case_data["request"]["verify_code"],
        phone_code=case_data["request"]["phone_code"],
        password=test_context.password,
        dy_server=case_data["request"]["dy_server"],
    )


@pytest.fixture
def login_done(register_done, member_api: MemberRequestApi, test_context: TestContext):
    case_data = _first_case(DATA_DIR / "test_04_login.json")
    return member_api.login(
        phone=test_context.phone,
        password=case_data["request"]["password"] or test_context.password,
    )


@pytest.fixture
def is_login_done(login_done, member_api: MemberRequestApi):
    return member_api.is_login()


@pytest.fixture
def approve_realname_done(is_login_done, member_api: MemberRequestApi, test_context: TestContext):
    test_context.realname = generate_random_chinese_name()
    test_context.card_id = generate_random_id_card()
    return member_api.approve_realname(
        realname=test_context.realname,
        card_id=test_context.card_id,
    )


@pytest.fixture
def get_approve_info_done(approve_realname_done, member_api: MemberRequestApi):
    return member_api.get_approve_info()


@pytest.fixture
def open_account_done(get_approve_info_done, member_api: MemberRequestApi):
    return member_api.open_account()


@pytest.fixture
def switch_account_done(open_account_done, member_api: MemberRequestApi):
    case_data = _first_case(DATA_DIR / "test_09_apply_amount.json")
    return member_api.switch_account(user_role=case_data["pre_request"]["user_role"])


@pytest.fixture
def open_amount_page_done(switch_account_done, member_api: MemberRequestApi):
    return member_api.open_amount_page()


@pytest.fixture
def amount_image_code_done(open_amount_page_done, member_api: MemberRequestApi):
    return member_api.get_amount_image_code()


@pytest.fixture
def apply_amount_done(amount_image_code_done, member_api: MemberRequestApi):
    case_data = _first_case(DATA_DIR / "test_09_apply_amount.json")
    request_data = case_data["request"]
    return member_api.apply_amount(
        amount_type=request_data["amount_type"],
        amount_account=request_data["amount_account"],
        remark=request_data["remark"],
        verify_code=request_data["verify_code"],
    )


@pytest.fixture
def admin_login_image_code_done(apply_amount_done, admin_api: AdminRequestApi):
    return admin_api.get_login_image_code()


@pytest.fixture
def admin_login_done(admin_login_image_code_done, admin_api: AdminRequestApi):
    case_data = _first_case(DATA_DIR / "test_10_admin_login.json")
    request_data = case_data["request"]
    return admin_api.login(
        username=request_data["username"],
        password=request_data["password"],
        valicode=request_data["valicode"],
    )


@pytest.fixture
def search_amount_apply_list_done(admin_login_done, admin_api: AdminRequestApi, test_context: TestContext):
    case_data = _first_case(DATA_DIR / "test_11_search_amount_apply_list.json")
    request_data = case_data["request"]
    response = admin_api.search_amount_apply_list(
        member_name=test_context.phone,
        category_id=request_data["category_id"],
    )
    payload = response.json()
    first_item = payload["data"]["items"][0]
    test_context.editid = str(first_item.get("id", ""))
    test_context.member_id = str(first_item.get("member_id", ""))
    test_context.amount = str(first_item.get("amount", ""))
    test_context.remark = str(first_item.get("remark", ""))
    test_context.record_id = str(first_item.get("id", ""))
    return response


@pytest.fixture
def open_amount_verify_page_done(search_amount_apply_list_done, admin_api: AdminRequestApi, test_context: TestContext):
    return admin_api.open_amount_verify_page(editid=test_context.editid)


@pytest.fixture
def verify_image_code_done(open_amount_verify_page_done, admin_api: AdminRequestApi):
    return admin_api.get_verify_image_code()


@pytest.fixture
def submit_amount_verify_done(verify_image_code_done, admin_api: AdminRequestApi, test_context: TestContext):
    case_data = _first_case(DATA_DIR / "test_13_submit_amount_verify.json")
    request_data = case_data["request"]
    return admin_api.submit_amount_verify(
        editid=test_context.editid,
        member_id=test_context.member_id,
        amount=test_context.amount,
        add_ip=request_data["add_ip"],
        category_id=request_data["category_id"],
        remark=test_context.remark,
        record_id=test_context.record_id,
        member_name=test_context.phone,
        verify_type=request_data["verify_type"],
        add_time=request_data["add_time"],
        income_amount=request_data["income_amount"],
        status=request_data["status"],
        verify_remark=request_data["verify_remark"],
        valicode=request_data["valicode"],
    )


@pytest.fixture
def get_amount_apply_log_done(submit_amount_verify_done, admin_api: AdminRequestApi, test_context: TestContext):
    return admin_api.get_amount_apply_log(member_name=test_context.phone)


@pytest.fixture
def register_image_code_response(request, member_api: MemberRequestApi):
    return member_api.get_register_image_code()


@pytest.fixture
def send_sms_response(request, register_image_code_done, member_api: MemberRequestApi, test_context: TestContext):
    case_data = request.param
    return member_api.send_sms(
        phone=test_context.phone,
        img_verify_code=case_data["request"]["img_verify_code"],
        sms_type=case_data["request"]["type"],
    )


@pytest.fixture
def register_response(request, send_sms_done, member_api: MemberRequestApi, test_context: TestContext):
    case_data = request.param
    return member_api.register(
        phone=test_context.phone,
        verify_code=case_data["request"]["verify_code"],
        phone_code=case_data["request"]["phone_code"],
        password=case_data["request"]["password"] or test_context.password,
        dy_server=case_data["request"]["dy_server"],
    )


@pytest.fixture
def login_response(request, register_done, member_api: MemberRequestApi, test_context: TestContext):
    case_data = request.param
    return member_api.login(
        phone=test_context.phone,
        password=case_data["request"]["password"] or test_context.password,
    )


@pytest.fixture
def is_login_response(request, member_api: MemberRequestApi):
    case_data = request.param
    if case_data.get("precondition") == "logged_in":
        request.getfixturevalue("login_done")
    return member_api.is_login()


@pytest.fixture
def approve_realname_response(request, member_api: MemberRequestApi, test_context: TestContext):
    case_data = request.param
    if case_data.get("precondition") == "logged_in":
        request.getfixturevalue("is_login_done")
    test_context.realname = generate_random_chinese_name()
    test_context.card_id = generate_random_id_card()
    return member_api.approve_realname(
        realname=test_context.realname,
        card_id=test_context.card_id,
    )


@pytest.fixture
def get_approve_info_response(request, member_api: MemberRequestApi, test_context: TestContext):
    request.getfixturevalue("approve_realname_done")
    return member_api.get_approve_info()


@pytest.fixture
def open_account_response(request, member_api: MemberRequestApi):
    request.getfixturevalue("get_approve_info_done")
    return member_api.open_account()


@pytest.fixture
def apply_amount_response(request, member_api: MemberRequestApi):
    case_data = request.param
    request.getfixturevalue("amount_image_code_done")
    request_data = case_data["request"]
    return member_api.apply_amount(
        amount_type=request_data["amount_type"],
        amount_account=request_data["amount_account"],
        remark=request_data["remark"],
        verify_code=request_data["verify_code"],
    )


@pytest.fixture
def admin_login_response(request, admin_api: AdminRequestApi):
    case_data = request.param
    request.getfixturevalue("admin_login_image_code_done")
    request_data = case_data["request"]
    return admin_api.login(
        username=request_data["username"],
        password=request_data["password"],
        valicode=request_data["valicode"],
    )


@pytest.fixture
def search_amount_apply_list_response(request, admin_api: AdminRequestApi, test_context: TestContext):
    case_data = request.param
    request.getfixturevalue("admin_login_done")
    request_data = case_data["request"]
    response = admin_api.search_amount_apply_list(
        member_name=test_context.phone,
        category_id=request_data["category_id"],
    )
    payload = response.json()
    first_item = payload["data"]["items"][0]
    test_context.editid = str(first_item.get("id", ""))
    test_context.member_id = str(first_item.get("member_id", ""))
    test_context.amount = str(first_item.get("amount", ""))
    test_context.remark = str(first_item.get("remark", ""))
    test_context.record_id = str(first_item.get("id", ""))
    return response


@pytest.fixture
def open_amount_verify_page_response(request, admin_api: AdminRequestApi, test_context: TestContext):
    request.getfixturevalue("search_amount_apply_list_done")
    return admin_api.open_amount_verify_page(editid=test_context.editid)


@pytest.fixture
def submit_amount_verify_response(request, admin_api: AdminRequestApi, test_context: TestContext):
    case_data = request.param
    request.getfixturevalue("verify_image_code_done")
    request_data = case_data["request"]
    return admin_api.submit_amount_verify(
        editid=test_context.editid,
        member_id=test_context.member_id,
        amount=test_context.amount,
        add_ip=request_data["add_ip"],
        category_id=request_data["category_id"],
        remark=test_context.remark,
        record_id=test_context.record_id,
        member_name=test_context.phone,
        verify_type=request_data["verify_type"],
        add_time=request_data["add_time"],
        income_amount=request_data["income_amount"],
        status=request_data["status"],
        verify_remark=request_data["verify_remark"],
        valicode=request_data["valicode"],
    )


@pytest.fixture
def get_amount_apply_log_response(request, admin_api: AdminRequestApi, test_context: TestContext):
    request.getfixturevalue("submit_amount_verify_done")
    return admin_api.get_amount_apply_log(member_name=test_context.phone)
