import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    formatter = logging.Formatter(FORMAT)

    file_handler = RotatingFileHandler(
        LOG_DIR / f"{name}.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console)
    return logger