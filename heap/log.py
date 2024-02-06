# Heap @ 2023
# chhongzh

"""
提供了一些基本的日志
"""

from logging import getLogger, StreamHandler, Formatter, WARN, DEBUG
from io import StringIO
from .version_info import HEAP_VERSION_STR

if not globals().get("HEAP_LOGGING_IS_INIT", None):
    HEAP_LOGGING_IS_INIT = True
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

    module_debug = lambda md_name, msg: debug(f"[Module]: [{md_name}]: {msg}")
    module_info = lambda md_name, msg: info(f"[Module]: [{md_name}]: {msg}")
    module_warning = lambda md_name, msg: warning(f"[Module]: [{md_name}]: {msg}")
    module_error = lambda md_name, msg: error(f"[Module]: [{md_name}]: {msg}")
    module_critical = lambda md_name, msg: critical(f"[Module]: [{md_name}]: {msg}")

    info(f"Heap V{HEAP_VERSION_STR}. Powered by Python. Made by chhongzh.")
