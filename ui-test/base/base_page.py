"""Base page object with common Selenium operations."""

from datetime import datetime
from pathlib import Path
from typing import Tuple

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from config import EXPLICIT_WAIT, SCREENSHOT_DIR, SHORT_EXPLICIT_WAIT, WAIT_POLL_FREQUENCY

Locator = Tuple[By, str]


class BasePage:
    """Shared UI actions used by all page objects."""

    def __init__(self, driver: WebDriver, timeout: int = EXPLICIT_WAIT):
        self.driver = driver
        self.timeout = timeout

    def open(self, url: str) -> None:
        self.driver.get(url)
        self.wait_visible((By.TAG_NAME, "body"), timeout=SHORT_EXPLICIT_WAIT)

    def wait_present(self, locator: Locator, timeout: int | None = None):
        return WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(ec.presence_of_element_located(locator))

    def wait_visible(self, locator: Locator, timeout: int | None = None):
        return WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(
            ec.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator: Locator, timeout: int | None = None):
        return WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=WAIT_POLL_FREQUENCY,
        ).until(
            ec.element_to_be_clickable(locator)
        )

    def find(self, locator: Locator):
        return self.wait_present(locator)

    def input_text(self, locator: Locator, text: str, clear_first: bool = True) -> None:
        element = self.wait_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def click(self, locator: Locator) -> None:
        self.wait_clickable(locator).click()

    def get_text(self, locator: Locator, timeout: int = SHORT_EXPLICIT_WAIT) -> str:
        try:
            return self.wait_visible(locator, timeout=timeout).text.strip()
        except TimeoutException:
            return ""

    def is_visible(self, locator: Locator, timeout: int = 1) -> bool:
        try:
            self.wait_visible(locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_page_text(self) -> str:
        return self.wait_visible((By.TAG_NAME, "body"), timeout=SHORT_EXPLICIT_WAIT).text.strip()

    def get_current_url(self) -> str:
        return self.driver.current_url

    def save_screenshot(self, file_path: Path) -> Path:
        """Save screenshot to a specific path."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(file_path))
        return file_path

    def screenshot_with_timestamp(self, prefix: str = "screenshot") -> Path:
        """Save screenshot with auto-generated timestamp file name."""
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.save_screenshot(SCREENSHOT_DIR / f"{prefix}_{timestamp}.png")
