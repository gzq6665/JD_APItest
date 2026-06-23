"""Login page object (locators + page actions)."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from config import LOGIN_URL


class LoginPage(BasePage):
    """Encapsulates interactions on the login page."""

    LOGIN_URL = LOGIN_URL

    # Page element locators.
    USERNAME_INPUT = (By.ID, "keywords")
    PASSWORD_INPUT = (By.ID, "password")
    CAPTCHA_INPUT = (By.ID, "verifycode")
    LOGIN_BUTTON = (By.ID, "login-btn")
    ERROR_BOX = (By.ID, "err")
    ERROR_SPAN = (By.CSS_SELECTOR, "#err span")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a.logout")
    USER_INFO = (By.CSS_SELECTOR, "li.last .user")

    CAPTCHA_TRIGGER_ATTEMPTS = 5

    def open_login(self) -> None:
        """Open login page URL."""
        self.open(self.LOGIN_URL)

    def input_username(self, username: str) -> None:
        self.input_text(self.USERNAME_INPUT, username)

    def input_password(self, password: str) -> None:
        self.input_text(self.PASSWORD_INPUT, password)

    def input_captcha(self, captcha: str) -> None:
        self.input_text(self.CAPTCHA_INPUT, captcha)

    def click_login(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def is_captcha_visible(self) -> bool:
        return self.is_visible(self.CAPTCHA_INPUT, timeout=2)

    def trigger_captcha(self, username: str, password: str, attempts: int | None = None) -> bool:
        """Trigger captcha input by repeated wrong-password login attempts."""
        real_attempts = attempts or self.CAPTCHA_TRIGGER_ATTEMPTS
        for index in range(real_attempts):
            self.open_login()
            self.input_username(username)
            self.input_password(f"{password}_wrong_{index}")
            self.click_login()
            if self.is_captcha_visible():
                return True
        return False

    def login(self, username: str, password: str, captcha: str | None = None) -> None:
        """Perform login submit flow."""
        self.input_username(username)
        self.input_password(password)
        if captcha is not None and self.is_captcha_visible():
            self.input_captcha(captcha)
        self.click_login()

    def wait_login_feedback(self, timeout: int = 8) -> None:
        """Wait until login result becomes visible."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.is_login_successful():
                return
            if self.get_error_text():
                return
            time.sleep(0.2)

    def is_login_successful(self) -> bool:
        """Check whether the page already switched into logged-in state."""
        return self.is_visible(self.LOGOUT_LINK, timeout=2) or self.is_visible(self.USER_INFO, timeout=2)

    def get_error_text(self) -> str:
        """Get visible login error text."""
        text = self.get_text(self.ERROR_SPAN, timeout=2)
        if text:
            return text

        text = self.get_text(self.ERROR_BOX, timeout=2)
        return text

    def get_logout_text(self) -> str:
        """Get the exact logout-link text after login succeeds."""
        return self.get_text(self.LOGOUT_LINK, timeout=2)

    def get_user_info_text(self) -> str:
        """Get the exact user-info text after login succeeds."""
        return self.get_text(self.USER_INFO, timeout=2)

    def get_success_text(self) -> str:
        """Get post-login visible text for success assertion."""
        parts = []
        logout_text = self.get_text(self.LOGOUT_LINK, timeout=2)
        user_text = self.get_text(self.USER_INFO, timeout=2)

        if logout_text:
            parts.append(logout_text)
        if user_text:
            parts.append(user_text)

        if parts:
            return " ".join(parts)
        return self.get_page_text()
