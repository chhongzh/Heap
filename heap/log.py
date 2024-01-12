# Heap @ 2023
# chhongzh

"""
提供了一些基本的日志
"""

from logging import getLogger, StreamHandler, Formatter, WARN
from io import StringIO
from .version_info import HEAP_VERSION_STR

HEAP_IO = StringIO()
HEAP_LOGGER = getLogger("Heap")
HEAP_HANDLER = StreamHandler(HEAP_IO)
HEAP_FORMATTER = Formatter("[%(asctime)s] [%(levelname)5s]: %(message)s")

HEAP_HANDLER.setFormatter(HEAP_FORMATTER)
HEAP_LOGGER.setLevel(WARN)

HEAP_LOGGER.addHandler(HEAP_HANDLER)

debug = lambda msg: HEAP_LOGGER.debug(msg)
info = lambda msg: HEAP_LOGGER.info(msg)
warning = lambda msg: HEAP_LOGGER.warning(msg)
error = lambda msg: HEAP_LOGGER.error(msg)
critical = lambda msg: HEAP_LOGGER.critical(msg)

info(f"Heap V{HEAP_VERSION_STR}. Powered by Python. Made by chhongzh.")
