"""Browser driver factory for Selenium tests."""

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config import (
    CHROMEDRIVER_PATH,
    IMPLICIT_WAIT,
    PAGE_LOAD_TIMEOUT,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class DriverFactory:
    """Create configured WebDriver instances."""

    @staticmethod
    def create_driver() -> webdriver.Chrome:
        """Create one Chrome driver with a maximize-first window strategy."""
        options = Options()
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(
            service=Service(executable_path=CHROMEDRIVER_PATH),
            options=options,
        )
        DriverFactory._expand_window(driver)
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        return driver

    @staticmethod
    def _expand_window(driver: webdriver.Chrome) -> None:
        """Keep the browser maximized, with a fixed-size fallback only if maximize fails."""
        try:
            driver.maximize_window()
            return
        except WebDriverException:
            pass

        try:
            driver.set_window_rect(x=0, y=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
            driver.execute_script(
                "window.moveTo(0, 0);"
                "window.resizeTo(arguments[0], arguments[1]);",
                WINDOW_WIDTH,
                WINDOW_HEIGHT,
            )
        except WebDriverException:
            pass
