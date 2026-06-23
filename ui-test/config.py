"""Project-wide runtime and path configuration."""

from pathlib import Path

# Target site configuration.
BASE_URL = "http://121.43.169.97:8081"
LOGIN_PATH = "/common/member/login"
LOGIN_URL = "http://121.43.169.97:8081/common/member/login"
REGISTER_PATH = "/common/member/reg"
REGISTER_URL = "http://121.43.169.97:8081/common/member/reg"
CENTER_PATH = "/member/member/center"
CENTER_URL = "http://121.43.169.97:8081/member/member/center"
TRUST_REG_PATH = "/trust/public/reg"
TRUST_REG_URL = "http://121.43.169.97:8081/trust/public/reg"
LOAN_AMOUNT_APPLY_PATH = "/loan/amount/index?type=1"
LOAN_AMOUNT_APPLY_URL = "http://121.43.169.97:8081/loan/amount/index?type=1"
ADMIN_BASE_URL = "http://121.43.169.97:8082"
ADMIN_LOGIN_PATH = "/"
ADMIN_LOGIN_URL = "http://121.43.169.97:8082/"
ADMIN_INDEX_PATH = "/system/index/index"
ADMIN_INDEX_URL = "http://121.43.169.97:8082/system/index/index"
CHROMEDRIVER_PATH = r"D:\Python313\chromedriver.exe"

# Local output directories.
ROOT_DIR = Path(__file__).resolve().parent
LOG_DIR = ROOT_DIR / "log"
REPORT_DIR = ROOT_DIR / "report"
REPORT_RESULTS_DIR = REPORT_DIR / "allure-results"
REPORT_OFFLINE_DIR = REPORT_DIR / "allure-offline"
SCREENSHOT_DIR = REPORT_DIR / "screenshots"

# Selenium runtime waits.
IMPLICIT_WAIT = 0
EXPLICIT_WAIT = 8
SHORT_EXPLICIT_WAIT = 2
PAGE_LOAD_TIMEOUT = 20
WAIT_POLL_FREQUENCY = 0.1
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FORCE_FULLSCREEN = False

# Default captcha value used by test data templates.
CAPTCHA_FIXED = "666666"
