"""Common utilities: directory prep, logger, and Allure report generation."""

import logging
import shutil
import subprocess
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Iterable, Optional, Tuple

from config import LOG_DIR, REPORT_OFFLINE_DIR, REPORT_RESULTS_DIR


def ensure_directories(paths: Iterable[Path]) -> None:
    """Create directories if they do not exist."""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "web_auto") -> logging.Logger:
    """Build/reuse a rotating logger for test runs."""
    ensure_directories([LOG_DIR])
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = TimedRotatingFileHandler(
        filename=str(LOG_DIR / "run.log"),
        when="midnight",
        interval=1,
        backupCount=14,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.propagate = False
    return logger


def generate_allure_offline_report(
    results_dir: Path = REPORT_RESULTS_DIR,
    report_dir: Path = REPORT_OFFLINE_DIR,
    logger: Optional[logging.Logger] = None,
) -> Tuple[bool, str]:
    """Generate single-file offline Allure report from result files."""
    ensure_directories([results_dir, report_dir])
    log = logger or get_logger()

    if not any(results_dir.iterdir()):
        msg = f"No Allure result files found in: {results_dir}"
        log.warning(msg)
        return False, msg

    allure_executable = shutil.which("allure") or shutil.which("allure.bat") or shutil.which("allure.cmd")
    if not allure_executable:
        msg = "Allure command was not found in PATH. Skip offline report generation."
        log.warning(msg)
        return False, msg

    cmd = [
        allure_executable,
        "generate",
        str(results_dir),
        "-o",
        str(report_dir),
        "--clean",
        "--single-file",
    ]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        msg = "Allure executable does not exist. Skip offline report generation."
        log.warning(msg)
        return False, msg

    if completed.returncode == 0:
        msg = f"Allure offline report generated: {report_dir / 'index.html'}"
        log.info(msg)
        return True, msg

    stderr = completed.stderr.strip()
    stdout = completed.stdout.strip()
    msg = f"Allure report generation failed. stdout={stdout} stderr={stderr}"
    log.error(msg)
    return False, msg
