"""Admin login page object (locators + page actions)."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from config import ADMIN_INDEX_URL, ADMIN_LOGIN_URL


class AdminLoginPage(BasePage):
    """Encapsulates interactions on the backend admin login page."""

    ADMIN_LOGIN_URL = ADMIN_LOGIN_URL
    ADMIN_INDEX_URL = ADMIN_INDEX_URL

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    CAPTCHA_INPUT = (By.ID, "valicode")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input.login-button")
    ERROR_MESSAGE = (By.ID, "errorMessage")
    BRAND_TEXT = (By.CSS_SELECTOR, ".navbar-brand small")
    USER_INFO = (By.CSS_SELECTOR, ".user-info")

    def open_login(self) -> None:
        """Open the backend admin login page."""
        self.open(self.ADMIN_LOGIN_URL)

    def input_username(self, username: str) -> None:
        """Input the admin account."""
        self.input_text(self.USERNAME_INPUT, username)

    def input_password(self, password: str) -> None:
        """Input the admin password."""
        self.input_text(self.PASSWORD_INPUT, password)

    def input_captcha(self, captcha: str) -> None:
        """Input the backend login captcha."""
        self.input_text(self.CAPTCHA_INPUT, captcha)

    def click_login(self) -> None:
        """Click the backend login button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str, captcha: str) -> None:
        """Perform admin login submit flow."""
        self.input_username(username)
        self.input_password(password)
        self.input_captcha(captcha)
        self.click_login()

    def wait_login_feedback(self, timeout: int = 8) -> None:
        """Wait until login success or error message is visible."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.is_login_successful():
                return
            if self.get_error_text():
                return
            time.sleep(0.2)

    def is_login_successful(self) -> bool:
        """Check whether the backend has switched to the admin index page."""
        return self.get_current_url() == self.ADMIN_INDEX_URL and self.is_visible(self.BRAND_TEXT, timeout=2)

    def get_error_text(self) -> str:
        """Get the exact backend login error text."""
        return self.get_text(self.ERROR_MESSAGE, timeout=2)

    def get_brand_text(self) -> str:
        """Get the exact brand text shown after successful login."""
        return self.get_text(self.BRAND_TEXT, timeout=2)

    def get_user_info_text(self) -> str:
        """Get the exact user-info text shown after successful login."""
        return self.get_text(self.USER_INFO, timeout=2)
