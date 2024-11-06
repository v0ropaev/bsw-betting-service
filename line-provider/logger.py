import sys

from loguru import logger


logger.add(
    sys.stdout,
    format="{time:YYYY.MM.DD HH:mm:ss} | {level} | {file}:{function}:{line} | {message}",
    level="INFO",
)
