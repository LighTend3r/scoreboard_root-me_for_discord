import logging
import logging.handlers as handlers
import re
import sys
import traceback

from utils.config import TEMP_LOG_FILENAME
from inspect import getframeinfo, stack

def LINE():
    caller = getframeinfo(stack()[2][0])
    return caller.lineno


def FILE():
    caller = getframeinfo(stack()[2][0])
    return caller.filename


def FUNCTION():
    caller = getframeinfo(stack()[2][0])
    return caller.function


logger = logging.getLogger("discord_bot")

l_handler = logging.StreamHandler()
temp_handler = handlers.WatchedFileHandler(TEMP_LOG_FILENAME)
l_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] (%(path)s:%(line)d) %(function)s(): %(message)s",
    datefmt="[%m/%d/%Y %I:%M:%S %p]",
)

l_handler.setFormatter(l_formatter)
temp_handler.setFormatter(l_formatter)

# Logging format
logger.addHandler(l_handler)
logger.addHandler(temp_handler)

# Add specific log level for moderator activities

logger.setLevel(logging.INFO)


def info(msg: str) -> None:
    d = {"line": LINE(), "path": FILE(), "function": FUNCTION()}
    logger.info(f"{msg}", extra=d)


def warning(msg: str) -> None:
    d = {"line": LINE(), "path": FILE(), "function": FUNCTION()}
    logger.warning(f"{msg}", extra=d)


def error(msg: str) -> None:
    d = {"line": LINE(), "path": FILE(), "function": FUNCTION()}
    exc_type, exc_value, exc_traceback = sys.exc_info()
    str_exc_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.error(f"{msg}\n{str_exc_traceback}", extra=d)


def debug(msg: str) -> None:
    d = {"line": LINE(), "path": FILE(), "function": FUNCTION()}
    logger.debug(f"{msg}", extra=d)

