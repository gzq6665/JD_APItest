"""Shared pytest fixtures and hooks for web UI automation."""

from __future__ import annotations

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any

import allure
import pytest

from base.driver_factory import DriverFactory
from config import LOG_DIR, REPORT_OFFLINE_DIR, REPORT_RESULTS_DIR, ROOT_DIR, SCREENSHOT_DIR
from page.admin_amount_apply_audit_page import AdminAmountApplyAuditPage
from page.admin_login_page import AdminLoginPage
from page.login_page import LoginPage
from page.loan_amount_apply_page import LoanAmountApplyPage
from page.open_account_page import OpenAccountPage
from page.register_page import RegisterPage
from tool import ensure_directories, generate_allure_offline_report, get_logger

# Login test data source (JSON only, data folder is kept as a normal folder).
LOGIN_DATA_FILE = ROOT_DIR / "data" / "login_data.json"
REGISTER_DATA_FILE = ROOT_DIR / "data" / "register_data.json"
OPEN_ACCOUNT_DATA_FILE = ROOT_DIR / "data" / "open_account_data.json"
LOAN_AMOUNT_APPLY_DATA_FILE = ROOT_DIR / "data" / "loan_amount_apply_data.json"
ADMIN_LOGIN_DATA_FILE = ROOT_DIR / "data" / "admin_login_data.json"
ADMIN_AMOUNT_APPLY_AUDIT_DATA_FILE = ROOT_DIR / "data" / "admin_amount_apply_audit_data.json"


def _read_json_file(file_path: Path) -> dict[str, Any]:
    """Read one JSON file and tolerate UTF-8 BOM emitted by some editors."""
    return json.loads(file_path.read_text(encoding="utf-8-sig"))


def _load_login_data() -> dict[str, Any]:
    """Load the login dataset from JSON."""
    return _read_json_file(LOGIN_DATA_FILE)


def _load_register_data() -> dict[str, Any]:
    """Load the register dataset from JSON."""
    return _read_json_file(REGISTER_DATA_FILE)


def _load_open_account_data() -> dict[str, Any]:
    """Load the open-account dataset from JSON."""
    return _read_json_file(OPEN_ACCOUNT_DATA_FILE)


def _load_loan_amount_apply_data() -> dict[str, Any]:
    """Load the loan amount apply dataset from JSON."""
    return _read_json_file(LOAN_AMOUNT_APPLY_DATA_FILE)


def _load_admin_login_data() -> dict[str, Any]:
    """Load the admin login dataset from JSON."""
    return _read_json_file(ADMIN_LOGIN_DATA_FILE)


def _load_admin_amount_apply_audit_data() -> dict[str, Any]:
    """Load the admin amount-apply-audit dataset from JSON."""
    return _read_json_file(ADMIN_AMOUNT_APPLY_AUDIT_DATA_FILE)


def _is_placeholder(value: str) -> bool:
    return value.startswith("REPLACE_WITH_")


def _resolve_value(raw_value: str | None, credentials: dict[str, str]) -> str | None:
    """Resolve template placeholders in a single case value."""
    if raw_value is None:
        return None
    return (
        raw_value.replace("${VALID_USERNAME}", credentials["valid_username"])
        .replace("${VALID_PASSWORD}", credentials["valid_password"])
        .replace("${CAPTCHA_FIXED}", credentials["captcha_fixed"])
    )


def _build_case(raw_case: dict[str, Any], credentials: dict[str, str]) -> dict[str, Any]:
    """Build a runnable case object for tests."""
    return {
        "case_id": raw_case["case_id"],
        "title": raw_case["title"],
        "username": _resolve_value(raw_case["username"], credentials),
        "password": _resolve_value(raw_case["password"], credentials),
        "captcha": _resolve_value(raw_case["captcha"], credentials),
        "need_captcha": raw_case["need_captcha"],
        "expect_text": raw_case["expect_text"],
        "expect_tokens": [token.strip() for token in raw_case["expect_text"].split("|") if token.strip()],
        "expect_result": raw_case["expect_result"],
        "expect_logout_text": _resolve_value(raw_case.get("expect_logout_text"), credentials),
        "expect_user_text": _resolve_value(raw_case.get("expect_user_text"), credentials),
        "valid_username": credentials["valid_username"],
        "valid_password": credentials["valid_password"],
    }


def _random_phone() -> str:
    """Generate a random 11-digit phone for register success/format tests."""
    return f"13{random.randint(0, 999999999):09d}"


def _random_card_id() -> str:
    """Generate a simple 18-digit numeric ID for test data."""
    return f"1101011990{random.randint(10000000, 99999999):08d}"


def _resolve_register_value(raw_value: str | None, defaults: dict[str, str]) -> str | None:
    """Resolve template placeholders in register case values."""
    if raw_value is None:
        return None
    return (
        raw_value.replace("${VALID_PASSWORD}", defaults["valid_password"])
        .replace("${IMAGE_CODE_FIXED}", defaults["image_code_fixed"])
        .replace("${SMS_CODE_FIXED}", defaults["sms_code_fixed"])
        .replace("${RANDOM_PHONE}", _random_phone())
    )


def _build_register_case(raw_case: dict[str, Any], defaults: dict[str, str]) -> dict[str, Any]:
    """Build a runnable register case object for tests."""
    return {
        "case_id": raw_case["case_id"],
        "title": raw_case["title"],
        "phone": _resolve_register_value(raw_case["phone"], defaults),
        "password": _resolve_register_value(raw_case["password"], defaults),
        "image_code": _resolve_register_value(raw_case["image_code"], defaults),
        "sms_code": _resolve_register_value(raw_case["sms_code"], defaults),
        "send_sms": raw_case["send_sms"],
        "expect_text": raw_case["expect_text"],
        "expect_tokens": [token.strip() for token in raw_case["expect_text"].split("|") if token.strip()],
        "expect_result": raw_case["expect_result"],
        "expect_title_text": raw_case.get("expect_title_text"),
    }


def _resolve_open_account_value(raw_value: str | None, defaults: dict[str, str]) -> str | None:
    """Resolve template placeholders in open-account case values."""
    if raw_value is None:
        return None
    return (
        raw_value.replace("${VALID_REALNAME}", defaults["valid_realname"])
        .replace("${VALID_CARD_ID}", _random_card_id())
    )


def _build_open_account_case(raw_case: dict[str, Any], defaults: dict[str, str]) -> dict[str, Any]:
    """Build a runnable open-account case object for tests."""
    return {
        "case_id": raw_case["case_id"],
        "title": raw_case["title"],
        "realname": _resolve_open_account_value(raw_case["realname"], defaults),
        "card_id": _resolve_open_account_value(raw_case["card_id"], defaults),
        "expect_text": raw_case["expect_text"],
        "expect_tokens": [token.strip() for token in raw_case["expect_text"].split("|") if token.strip()],
        "expect_result": raw_case["expect_result"],
        "expect_button_text": raw_case.get("expect_button_text"),
        "expect_info_title_text": raw_case.get("expect_info_title_text"),
        "expect_redirect_url": raw_case.get("expect_redirect_url"),
        "expect_error_field": raw_case.get("expect_error_field"),
    }


def _resolve_loan_amount_apply_value(raw_value: str | None, defaults: dict[str, str]) -> str | None:
    """Resolve template placeholders in loan amount apply case values."""
    if raw_value is None:
        return None
    return (
        raw_value.replace("${VALID_AMOUNT}", defaults["valid_amount"])
        .replace("${VALID_REMARK}", defaults["valid_remark"])
        .replace("${VALID_VERIFYCODE}", defaults["valid_verifycode"])
    )


def _build_loan_amount_apply_case(raw_case: dict[str, Any], defaults: dict[str, str]) -> dict[str, Any]:
    """Build a runnable loan amount apply case object for tests."""
    return {
        "case_id": raw_case["case_id"],
        "title": raw_case["title"],
        "apply_type": raw_case.get("apply_type", defaults.get("apply_type", "first")),
        "amount_account": _resolve_loan_amount_apply_value(raw_case["amount_account"], defaults),
        "remark": _resolve_loan_amount_apply_value(raw_case["remark"], defaults),
        "verifycode": _resolve_loan_amount_apply_value(raw_case["verifycode"], defaults),
        "expect_text": raw_case["expect_text"],
        "expect_tokens": [token.strip() for token in raw_case["expect_text"].split("|") if token.strip()],
        "expect_result": raw_case["expect_result"],
        "expect_type_text": raw_case.get("expect_type_text"),
        "expect_amount_text": raw_case.get("expect_amount_text"),
        "expect_status_text": raw_case.get("expect_status_text"),
    }


def _resolve_admin_login_value(raw_value: str | None, credentials: dict[str, str]) -> str | None:
    """Resolve template placeholders in admin login case values."""
    if raw_value is None:
        return None
    return (
        raw_value.replace("${ADMIN_USERNAME}", credentials["valid_username"])
        .replace("${ADMIN_PASSWORD}", credentials["valid_password"])
        .replace("${ADMIN_CAPTCHA}", credentials["captcha_fixed"])
    )


def _build_admin_login_case(raw_case: dict[str, Any], credentials: dict[str, str]) -> dict[str, Any]:
    """Build a runnable admin-login case object for tests."""
    return {
        "case_id": raw_case["case_id"],
        "title": raw_case["title"],
        "username": _resolve_admin_login_value(raw_case["username"], credentials),
        "password": _resolve_admin_login_value(raw_case["password"], credentials),
        "captcha": _resolve_admin_login_value(raw_case["captcha"], credentials),
        "expect_text": raw_case["expect_text"],
        "expect_result": raw_case["expect_result"],
        "expect_url": raw_case.get("expect_url"),
        "expect_brand_text": raw_case.get("expect_brand_text"),
        "expect_user_text": raw_case.get("expect_user_text"),
    }


def _build_admin_amount_apply_audit_case(raw_case: dict[str, Any]) -> dict[str, Any]:
    """Build a runnable admin amount-apply-audit case object for tests."""
    return {
        "case_id": raw_case["case_id"],
        "title": raw_case["title"],
        "member_name": raw_case["member_name"],
        "income_amount": raw_case["income_amount"],
        "audit_status_value": raw_case["audit_status_value"],
        "audit_remark": raw_case["audit_remark"],
        "captcha": raw_case["captcha"],
        "log_status_value": raw_case["log_status_value"],
        "expect_status_text": raw_case["expect_status_text"],
        "expect_category_text": raw_case["expect_category_text"],
        "expect_pass_amount_text": raw_case["expect_pass_amount_text"],
    }


def pytest_generate_tests(metafunc):
    """Automatically parametrize login/register test cases from JSON."""
    if "case_data" in metafunc.fixturenames:
        login_dataset = _load_login_data()
        login_cases = login_dataset["cases"]
        login_ids = [case["case_id"] for case in login_cases]
        metafunc.parametrize("case_data", login_cases, ids=login_ids, indirect=True)

    if "register_case_data" in metafunc.fixturenames:
        register_dataset = _load_register_data()
        register_cases = register_dataset["cases"]
        register_ids = [case["case_id"] for case in register_cases]
        metafunc.parametrize("register_case_data", register_cases, ids=register_ids, indirect=True)

    if "open_account_case_data" in metafunc.fixturenames:
        open_account_dataset = _load_open_account_data()
        open_account_cases = open_account_dataset["cases"]
        open_account_ids = [case["case_id"] for case in open_account_cases]
        metafunc.parametrize("open_account_case_data", open_account_cases, ids=open_account_ids, indirect=True)

    if "loan_amount_apply_case_data" in metafunc.fixturenames:
        loan_amount_apply_dataset = _load_loan_amount_apply_data()
        loan_amount_apply_cases = loan_amount_apply_dataset["cases"]
        loan_amount_apply_ids = [case["case_id"] for case in loan_amount_apply_cases]
        metafunc.parametrize(
            "loan_amount_apply_case_data",
            loan_amount_apply_cases,
            ids=loan_amount_apply_ids,
            indirect=True,
        )

    if "admin_login_case_data" in metafunc.fixturenames:
        admin_login_dataset = _load_admin_login_data()
        admin_login_cases = admin_login_dataset["cases"]
        admin_login_ids = [case["case_id"] for case in admin_login_cases]
        metafunc.parametrize(
            "admin_login_case_data",
            admin_login_cases,
            ids=admin_login_ids,
            indirect=True,
        )

    if "admin_amount_apply_audit_case_data" in metafunc.fixturenames:
        admin_amount_apply_audit_dataset = _load_admin_amount_apply_audit_data()
        admin_amount_apply_audit_cases = admin_amount_apply_audit_dataset["cases"]
        admin_amount_apply_audit_ids = [case["case_id"] for case in admin_amount_apply_audit_cases]
        metafunc.parametrize(
            "admin_amount_apply_audit_case_data",
            admin_amount_apply_audit_cases,
            ids=admin_amount_apply_audit_ids,
            indirect=True,
        )


def pytest_configure(config):
    """Force Allure output to project-root report directory regardless of launch cwd."""
    if hasattr(config.option, "allure_report_dir"):
        config.option.allure_report_dir = str(REPORT_RESULTS_DIR)
    if hasattr(config.option, "clean_alluredir"):
        config.option.clean_alluredir = True


@pytest.fixture(scope="session")
def logger():
    """Session-wide logger."""
    return get_logger("web_auto")


@pytest.fixture(scope="session")
def login_dataset() -> dict[str, Any]:
    """Session-wide loaded JSON data."""
    return _load_login_data()


@pytest.fixture(scope="session")
def register_dataset() -> dict[str, Any]:
    """Session-wide loaded JSON data for register module."""
    return _load_register_data()


@pytest.fixture(scope="session")
def open_account_dataset() -> dict[str, Any]:
    """Session-wide loaded JSON data for open-account module."""
    return _load_open_account_data()


@pytest.fixture(scope="session")
def loan_amount_apply_dataset() -> dict[str, Any]:
    """Session-wide loaded JSON data for loan amount apply module."""
    return _load_loan_amount_apply_data()


@pytest.fixture(scope="session")
def admin_login_dataset() -> dict[str, Any]:
    """Session-wide loaded JSON data for admin login module."""
    return _load_admin_login_data()


@pytest.fixture(scope="session")
def admin_amount_apply_audit_dataset() -> dict[str, Any]:
    """Session-wide loaded JSON data for admin amount-apply-audit module."""
    return _load_admin_amount_apply_audit_data()


@pytest.fixture(scope="function")
def case_data(request, login_dataset) -> dict[str, Any]:
    """Per-case resolved data passed into test methods."""
    credentials = login_dataset["credentials"]
    case = _build_case(request.param, credentials)

    # Guardrails for scenarios that require real credentials.
    if case["expect_result"] == "success" and (
        _is_placeholder(credentials["valid_username"]) or _is_placeholder(credentials["valid_password"])
    ):
        pytest.skip("Please set valid credentials in data/login_data.json first.")
    if case["need_captcha"] and (
        _is_placeholder(credentials["valid_username"]) or _is_placeholder(credentials["valid_password"])
    ):
        pytest.skip("Captcha scenarios require valid credentials.")
    return case


@pytest.fixture(scope="function")
def register_case_data(request, register_dataset) -> dict[str, Any]:
    """Per-case resolved data passed into register tests."""
    defaults = register_dataset["defaults"]
    return _build_register_case(request.param, defaults)


@pytest.fixture(scope="function")
def open_account_case_data(request, open_account_dataset) -> dict[str, Any]:
    """Per-case resolved data passed into open-account tests."""
    defaults = open_account_dataset["defaults"]
    return _build_open_account_case(request.param, defaults)


@pytest.fixture(scope="function")
def loan_amount_apply_case_data(request, loan_amount_apply_dataset) -> dict[str, Any]:
    """Per-case resolved data passed into loan amount apply tests."""
    defaults = loan_amount_apply_dataset["defaults"]
    return _build_loan_amount_apply_case(request.param, defaults)


@pytest.fixture(scope="function")
def admin_login_case_data(request, admin_login_dataset) -> dict[str, Any]:
    """Per-case resolved data passed into admin login tests."""
    credentials = admin_login_dataset["credentials"]
    return _build_admin_login_case(request.param, credentials)


@pytest.fixture(scope="function")
def admin_amount_apply_audit_case_data(request, admin_amount_apply_audit_dataset) -> dict[str, Any]:
    """Per-case resolved data passed into admin amount-apply-audit tests."""
    return _build_admin_amount_apply_audit_case(request.param)


@pytest.fixture(scope="function")
def driver(logger):
    """Create and close browser instance per test case."""
    driver_instance = DriverFactory.create_driver()
    logger.info("Chrome driver started.")
    yield driver_instance
    driver_instance.quit()
    logger.info("Chrome driver closed.")


@pytest.fixture(scope="function")
def login_page(driver) -> LoginPage:
    """Provide page object instance for login tests."""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def admin_login_page(driver) -> AdminLoginPage:
    """Provide page object instance for admin login tests."""
    return AdminLoginPage(driver)


@pytest.fixture(scope="function")
def authenticated_admin_driver(driver, admin_login_dataset):
    """Log in to backend admin once and provide an authenticated browser instance."""
    credentials = admin_login_dataset["credentials"]
    page = AdminLoginPage(driver)
    page.open_login()
    page.login(
        username=credentials["valid_username"],
        password=credentials["valid_password"],
        captcha=credentials["captcha_fixed"],
    )
    page.wait_login_feedback()
    if not page.is_login_successful():
        error_text = page.get_error_text() or page.get_page_text()
        pytest.fail(f"Admin login prerequisite failed: {error_text}")
    return driver


@pytest.fixture(scope="function")
def admin_amount_apply_audit_page(authenticated_admin_driver) -> AdminAmountApplyAuditPage:
    """Provide page object instance for backend amount-apply-audit tests."""
    return AdminAmountApplyAuditPage(authenticated_admin_driver)


@pytest.fixture(scope="function")
def prepared_admin_amount_apply_audit_context(
    admin_amount_apply_audit_page,
    fresh_pending_amount_apply,
    logger,
) -> dict[str, Any]:
    """Prepare one exact pending amount-apply row for backend audit tests."""
    admin_amount_apply_audit_page.open_amount_apply_audit_page()
    admin_amount_apply_audit_page.search_audit_list(fresh_pending_amount_apply["phone"])

    selected_row = admin_amount_apply_audit_page.get_row_data_by_remark(fresh_pending_amount_apply["remark"])
    admin_amount_apply_audit_page.select_row_by_id(selected_row["id"])

    logger.info(
        "Admin amount apply audit selected row: id=%s, member=%s, category=%s, status=%s",
        selected_row["id"],
        selected_row["member"],
        selected_row["category"],
        selected_row["status"],
    )

    context = {
        "page": admin_amount_apply_audit_page,
        "selected_row": selected_row,
        "fresh_pending_amount_apply": fresh_pending_amount_apply,
    }
    yield context
    try:
        admin_amount_apply_audit_page.driver.switch_to.default_content()
    except Exception:
        pass


@pytest.fixture(scope="function")
def register_page(driver) -> RegisterPage:
    """Provide page object instance for register tests."""
    return RegisterPage(driver)


@pytest.fixture(scope="function")
def new_registered_user(driver, register_dataset) -> dict[str, str]:
    """Create a fresh registered user that has not opened a trust account yet."""
    defaults = register_dataset["defaults"]
    phone = _random_phone()
    password = defaults["valid_password"]

    page = RegisterPage(driver)
    page.open_register()
    page.register(
        phone=phone,
        password=password,
        image_code=defaults["image_code_fixed"],
        sms_code=defaults["sms_code_fixed"],
        send_sms=True,
    )
    page.wait_feedback(timeout=8)

    if page.get_error_text():
        pytest.fail(f"Register prerequisite failed: {page.get_error_text()}")

    return {
        "phone": phone,
        "password": password,
    }


@pytest.fixture(scope="function")
def newly_registered_driver(driver, new_registered_user):
    """Go to user center directly after register success."""
    page = RegisterPage(driver)
    page.go_to_user_center()
    return driver


@pytest.fixture(scope="function")
def open_account_page(newly_registered_driver) -> OpenAccountPage:
    """Provide page object instance for open-account tests."""
    return OpenAccountPage(newly_registered_driver)


@pytest.fixture(scope="function")
def authenticated_driver(driver, login_dataset):
    """Log in once and provide an authenticated browser instance."""
    credentials = login_dataset["credentials"]
    if _is_placeholder(credentials["valid_username"]) or _is_placeholder(credentials["valid_password"]):
        pytest.skip("Please set valid credentials in data/login_data.json first.")

    page = LoginPage(driver)
    page.open_login()
    page.login(
        username=credentials["valid_username"],
        password=credentials["valid_password"],
        captcha=credentials.get("captcha_fixed"),
    )
    page.wait_login_feedback()
    if not page.is_login_successful():
        error_text = page.get_error_text() or page.get_page_text()
        pytest.fail(f"Login prerequisite failed: {error_text}")
    return driver


@pytest.fixture(scope="function")
def opened_account_driver(newly_registered_driver, open_account_dataset):
    """Create a fresh user, open the trust account, then return the authenticated driver."""
    defaults = open_account_dataset["defaults"]
    page = OpenAccountPage(newly_registered_driver)
    page.open_open_account_page()
    page.submit_identity_info(
        realname=defaults["valid_realname"],
        card_id=_resolve_open_account_value("${VALID_CARD_ID}", defaults) or defaults["valid_card_id"],
    )
    page.wait_feedback(timeout=10)

    if page.get_error_text():
        pytest.fail(f"Open-account prerequisite failed: {page.get_error_text()}")
    if not page.is_ready_for_open():
        pytest.fail(f"Open-account prerequisite did not enter final step: {page.get_page_text()}")

    redirect_url = page.click_open_now_and_switch()
    if not page.is_external_register_page(redirect_url):
        pytest.fail(f"Open-account redirect assertion failed: {redirect_url}")
    page.close_external_and_back()
    return newly_registered_driver


@pytest.fixture(scope="function")
def loan_amount_apply_page(authenticated_driver) -> LoanAmountApplyPage:
    """Provide page object instance for loan amount apply tests with existing login credentials."""
    return LoanAmountApplyPage(authenticated_driver)


@pytest.fixture(scope="function")
def fresh_pending_amount_apply(login_dataset, logger) -> dict[str, str]:
    """Create one fresh frontend amount-apply request for backend audit preconditions."""
    credentials = login_dataset["credentials"]
    if _is_placeholder(credentials["valid_username"]) or _is_placeholder(credentials["valid_password"]):
        pytest.skip("Please set valid credentials in data/login_data.json first.")

    temp_driver = DriverFactory.create_driver()
    logger.info("Chrome driver started for frontend amount-apply precondition.")

    phone = credentials["valid_username"]
    amount = "5000"
    remark = f"后台审核前置_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    verifycode = "8888"

    try:
        login_page = LoginPage(temp_driver)
        login_page.open_login()
        login_page.login(
            username=credentials["valid_username"],
            password=credentials["valid_password"],
            captcha=credentials.get("captcha_fixed"),
        )
        login_page.wait_login_feedback()
        if not login_page.is_login_successful():
            error_text = login_page.get_error_text() or login_page.get_page_text()
            pytest.fail(f"Frontend login prerequisite failed: {error_text}")

        amount_page = LoanAmountApplyPage(temp_driver)
        amount_page.open_apply_page()
        previous_record_text = amount_page.get_latest_record_text()
        amount_page.submit_application(
            apply_type="first",
            amount_account=amount,
            remark=remark,
            verifycode=verifycode,
        )
        amount_page.wait_feedback(timeout=8)

        if amount_page.get_error_text():
            pytest.fail(f"Frontend amount-apply prerequisite failed: {amount_page.get_error_text()}")

        amount_page.wait_latest_record_updated(previous_record_text, timeout=10)
        latest_status = amount_page.get_latest_record_status()
        if latest_status != "待审核":
            pytest.fail(f"Frontend amount-apply status mismatch: {latest_status}")

        logger.info(
            "Prepared fresh amount apply: phone=%s, remark=%s, amount=%s, status=%s",
            phone,
            remark,
            amount,
            latest_status,
        )
        return {
            "phone": phone,
            "remark": remark,
            "amount": amount,
            "pass_amount": "5000.00",
        }
    finally:
        temp_driver.quit()
        logger.info("Chrome driver closed for frontend amount-apply precondition.")


def pytest_sessionstart(session):
    """Prepare output directories before test run."""
    ensure_directories([LOG_DIR, REPORT_RESULTS_DIR, REPORT_OFFLINE_DIR, SCREENSHOT_DIR])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot and attach to Allure when test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return

    driver_instance = item.funcargs.get("driver")
    logger = item.funcargs.get("logger", get_logger("web_auto"))
    if not driver_instance:
        return

    screenshot_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot_path = SCREENSHOT_DIR / screenshot_name
    try:
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        driver_instance.save_screenshot(str(screenshot_path))
        allure.attach.file(
            str(screenshot_path),
            name=f"failure_{item.name}",
            attachment_type=allure.attachment_type.PNG,
        )
        logger.error("Test failed. Screenshot saved: %s", screenshot_path)
    except Exception as exc:
        logger.error("Failed to save screenshot for %s: %s", item.name, exc)


def pytest_sessionfinish(session, exitstatus):
    """Generate offline Allure report after the test session."""
    logger = get_logger("web_auto")
    generate_allure_offline_report(logger=logger)


