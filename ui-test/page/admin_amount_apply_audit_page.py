"""Admin amount-apply-audit page object (locators + page actions)."""

from __future__ import annotations

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait

from base.base_page import BasePage
from config import ADMIN_INDEX_URL, WAIT_POLL_FREQUENCY


class AdminAmountApplyAuditPage(BasePage):
    """Encapsulates backend amount-apply-audit navigation, iframe switching, and review actions."""

    ADMIN_INDEX_URL = ADMIN_INDEX_URL

    TOP_NAV_ITEMS = (By.CSS_SELECTOR, ".ace-nav-list li a")
    SIDEBAR_ITEMS = (By.CSS_SELECTOR, ".sidebar .nav-list > li")
    SIDEBAR_TOGGLE = (By.CSS_SELECTOR, "a.dropdown-toggle")
    AMOUNT_AUDIT_MENU = (By.CSS_SELECTOR, "a[rel='loan/amountapply/list']")
    AMOUNT_LOG_MENU = (By.CSS_SELECTOR, "a[rel='loan/amountapplylog/list']")
    CONTENT_FRAMES = (By.CSS_SELECTOR, "iframe")

    MEMBER_NAME_INPUT = (By.NAME, "member_name")
    STATUS_SELECT = (By.NAME, "status")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "input.srcbtn")
    AUDIT_BUTTON = (By.CSS_SELECTOR, "a[ng-click*='editList']")
    TABLE_ROWS = (By.CSS_SELECTOR, ".info_list tbody tr")
    FIRST_ROW = (By.CSS_SELECTOR, ".info_list tbody tr:first-child")
    FIRST_ROW_ID = (By.CSS_SELECTOR, ".info_list tbody tr:first-child td.id span")
    FIRST_ROW_CATEGORY = (By.CSS_SELECTOR, ".info_list tbody tr:first-child td.category_id span")
    FIRST_ROW_STATUS = (By.CSS_SELECTOR, ".info_list tbody tr:first-child td.status span")

    DIALOG_FRAME = (By.ID, "xubox_iframe1")
    DIALOG_SAVE_BUTTON = (By.CSS_SELECTOR, "input.dybtn-save")
    DIALOG_PASS_AMOUNT_INPUT = (By.NAME, "income_amount")
    DIALOG_PASS_RADIO = (By.CSS_SELECTOR, "input[name='status'][value='1']")
    DIALOG_FAIL_RADIO = (By.CSS_SELECTOR, "input[name='status'][value='-1']")
    DIALOG_FIRST_RADIO = (By.XPATH, "(//input[@type='radio'])[1]")
    DIALOG_SECOND_RADIO = (By.XPATH, "(//input[@type='radio'])[2]")
    DIALOG_REMARK_TEXTAREA = (By.TAG_NAME, "textarea")
    DIALOG_CAPTCHA_INPUT = (By.NAME, "valicode")

    BORROW_NAV_INDEX = 1
    AMOUNT_MENU_INDEX = 4

    def open_amount_apply_audit_page(self) -> None:
        """Open the amount-apply-audit iframe page from backend navigation."""
        self.open(self.ADMIN_INDEX_URL)
        self.open_borrow_menu()
        self.expand_amount_menu()
        amount_li = self._get_amount_menu_item()
        self.driver.execute_script("arguments[0].click();", amount_li.find_element(*self.AMOUNT_AUDIT_MENU))
        self.switch_to_content_frame("loan/amountapply/list")
        self.wait_visible(self.MEMBER_NAME_INPUT)

    def open_amount_apply_log_page(self) -> None:
        """Open the amount-apply-log iframe page from backend navigation."""
        self.driver.switch_to.default_content()
        self.open_borrow_menu()
        self.expand_amount_menu()
        amount_li = self._get_amount_menu_item()
        self.driver.execute_script("arguments[0].click();", amount_li.find_element(*self.AMOUNT_LOG_MENU))
        self.switch_to_content_frame("loan/amountapplylog/list")
        self.wait_visible(self.MEMBER_NAME_INPUT)

    def open_borrow_menu(self) -> None:
        """Switch the backend top navigation to borrow management."""
        nav = self._wait_for_nav_item(self.BORROW_NAV_INDEX)
        self.driver.execute_script("arguments[0].click();", nav)
        self._wait_for_sidebar_item(self.AMOUNT_MENU_INDEX)

    def expand_amount_menu(self) -> None:
        """Expand the left sidebar amount-management section."""
        amount_li = self._get_amount_menu_item()
        toggle = amount_li.find_element(*self.SIDEBAR_TOGGLE)
        if "open" not in (amount_li.get_attribute("class") or ""):
            self.driver.execute_script("arguments[0].click();", toggle)
        WebDriverWait(
            self.driver,
            self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(lambda _driver: amount_li.find_elements(*self.AMOUNT_AUDIT_MENU))

    def switch_to_content_frame(self, src_keyword: str) -> None:
        """Switch to a backend iframe whose src contains the target keyword."""
        self.driver.switch_to.default_content()
        frame = WebDriverWait(
            self.driver,
            self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(lambda _driver: self._find_frame_by_src(src_keyword))
        self.driver.switch_to.frame(frame)

    def switch_to_audit_dialog_frame(self) -> None:
        """Switch into the popup dialog iframe inside the audit list iframe."""
        WebDriverWait(
            self.driver,
            self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(ec.frame_to_be_available_and_switch_to_it(self.DIALOG_FRAME))
        self.wait_visible(self.DIALOG_PASS_AMOUNT_INPUT)

    def search_audit_list(self, member_name: str) -> None:
        """Search amount-apply audit entries by member phone."""
        self.input_text(self.MEMBER_NAME_INPUT, member_name)
        self.click(self.SEARCH_BUTTON)
        self.wait_present(self.TABLE_ROWS)

    def search_audit_log(self, member_name: str, log_status_value: str) -> None:
        """Search amount-apply logs by member phone and review status."""
        self.input_text(self.MEMBER_NAME_INPUT, member_name)
        Select(self.find(self.STATUS_SELECT)).select_by_value(log_status_value)
        self.click(self.SEARCH_BUTTON)
        self.wait_present(self.TABLE_ROWS)

    def get_first_row_id(self) -> str:
        """Get the first result row ID."""
        return self.get_text(self.FIRST_ROW_ID)

    def get_first_row_category(self) -> str:
        """Get the first result row amount category."""
        return self.get_text(self.FIRST_ROW_CATEGORY)

    def get_first_row_status(self) -> str:
        """Get the first result row audit status text."""
        return self.get_text(self.FIRST_ROW_STATUS)

    def get_row_data_by_remark(self, remark: str) -> dict[str, str]:
        """Get one exact audit-list row payload by unique remark text."""
        return WebDriverWait(
            self.driver,
            self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(lambda _driver: self._extract_row_data_by_remark(remark))

    def get_row_data_by_id(self, row_id: str) -> dict[str, str]:
        """Get one exact log-row payload by application ID."""
        return WebDriverWait(
            self.driver,
            self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(lambda _driver: self._extract_row_data_by_id(row_id))

    def select_row_by_id(self, row_id: str) -> None:
        """Select one exact row in the current grid by application ID."""
        row = WebDriverWait(
            self.driver,
            self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(lambda _driver: self._find_row_by_id(row_id))
        self.driver.execute_script("arguments[0].click();", row)

    def click_audit(self) -> None:
        """Click the audit toolbar button on the audit list page."""
        self.driver.execute_script("arguments[0].click();", self.wait_present(self.AUDIT_BUTTON))

    def audit_selected_application(
        self,
        income_amount: str,
        audit_status_value: str,
        audit_remark: str,
        captcha: str,
    ) -> None:
        """Audit the row that is already selected in the current amount-apply grid."""
        self.click_audit()
        self.switch_to_audit_dialog_frame()
        self.input_text(self.DIALOG_PASS_AMOUNT_INPUT, income_amount)
        self._choose_audit_status(audit_status_value)
        self.input_text(self.DIALOG_REMARK_TEXTAREA, audit_remark)
        self.input_text(self.DIALOG_CAPTCHA_INPUT, captcha)
        self.click(self.DIALOG_SAVE_BUTTON)
        self.wait_dialog_closed()

    def wait_dialog_closed(self) -> None:
        """Wait until the audit popup iframe disappears and return to the list iframe."""
        self.driver.switch_to.parent_frame()
        WebDriverWait(
            self.driver,
            self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until_not(ec.presence_of_element_located(self.DIALOG_FRAME))

    def _choose_audit_status(self, audit_status_value: str) -> None:
        """Choose pass or fail in the audit dialog."""
        if audit_status_value == "1":
            self._click_radio_circle([self.DIALOG_PASS_RADIO, self.DIALOG_FIRST_RADIO])
            return
        self._click_radio_circle([self.DIALOG_FAIL_RADIO, self.DIALOG_SECOND_RADIO])

    def _click_radio_circle(self, locators: list[tuple[By, str]]) -> None:
        """Click the visible audit radio circle instead of relying on label text."""
        last_error: Exception | None = None
        for locator in locators:
            try:
                radio = self.wait_present(locator, timeout=2)
                self.driver.execute_script(
                    "arguments[0].checked = true;"
                    "arguments[0].dispatchEvent(new Event('click', {bubbles:true}));"
                    "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
                    radio,
                )
                return
            except Exception as exc:
                last_error = exc
        if last_error:
            raise last_error

    def _extract_row_data_by_remark(self, remark: str) -> dict[str, str] | bool:
        """Extract row data when the target unique remark appears in the table."""
        for row in self.driver.find_elements(*self.TABLE_ROWS):
            try:
                row_data = self._extract_row_payload(row)
                if row_data["remark"] == remark:
                    return row_data
            except StaleElementReferenceException:
                return False
        return False

    def _extract_row_data_by_id(self, row_id: str) -> dict[str, str] | bool:
        """Extract row data when the target application ID appears in the table."""
        for row in self.driver.find_elements(*self.TABLE_ROWS):
            try:
                row_data = self._extract_row_payload(row)
                if row_data["id"] == row_id:
                    return row_data
            except StaleElementReferenceException:
                return False
        return False

    def _find_row_by_id(self, row_id: str) -> WebElement | bool:
        """Return one table row element by exact application ID."""
        for row in self.driver.find_elements(*self.TABLE_ROWS):
            try:
                if row.find_element(By.CSS_SELECTOR, "td.id span").text.strip() == row_id:
                    return row
            except StaleElementReferenceException:
                return False
        return False

    def _extract_row_payload(self, row: WebElement) -> dict[str, str]:
        """Extract the common visible cells from one amount-apply table row."""
        return {
            "id": row.find_element(By.CSS_SELECTOR, "td.id span").text.strip(),
            "member": row.find_element(By.CSS_SELECTOR, "td.member_name span").text.strip(),
            "category": row.find_element(By.CSS_SELECTOR, "td.category_id span").text.strip(),
            "remark": row.find_element(By.CSS_SELECTOR, "td.remark span").text.strip(),
            "pass_amount": row.find_element(By.CSS_SELECTOR, "td.income_amount span").text.strip(),
            "status": row.find_element(By.CSS_SELECTOR, "td.status span").text.strip(),
        }

    def _get_amount_menu_item(self) -> WebElement:
        """Get the top-level left menu item for amount management."""
        return self._wait_for_sidebar_item(self.AMOUNT_MENU_INDEX)

    def _wait_for_nav_item(self, index: int) -> WebElement:
        """Wait until a top navigation item is available by index."""
        return WebDriverWait(
            self.driver,
            self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(lambda _driver: self._get_indexed_element(self.TOP_NAV_ITEMS, index))

    def _wait_for_sidebar_item(self, index: int) -> WebElement:
        """Wait until a sidebar item is available by index."""
        return WebDriverWait(
            self.driver,
            self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(lambda _driver: self._get_indexed_element(self.SIDEBAR_ITEMS, index))

    def _get_indexed_element(self, locator, index: int) -> WebElement | bool:
        """Get one element from a locator list by index when it exists."""
        elements = self.driver.find_elements(*locator)
        if len(elements) <= index:
            return False
        return elements[index]

    def _find_frame_by_src(self, src_keyword: str) -> WebElement | bool:
        """Return the first iframe whose src contains the target keyword."""
        for frame in self.driver.find_elements(*self.CONTENT_FRAMES):
            if src_keyword in (frame.get_attribute("src") or ""):
                return frame
        return False
