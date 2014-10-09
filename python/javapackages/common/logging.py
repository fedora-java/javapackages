from __future__ import absolute_import
import logging


class SkipPyXBWarningsFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith("Unable to convert DOM node")


def init_logging():
    """Initialize loggers"""

    # Omit PyXB "Unable to convert DOM node to binding" warnings
    logger = logging.getLogger("pyxb.binding.basis")
    f = SkipPyXBWarningsFilter()
    logger.addFilter(f)
