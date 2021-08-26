import logging
from logging.handlers import SysLogHandler


def get_logger(name, level=None):
    logger = logging.getLogger(name)
    level = logging.WARN if level is None else getattr(logging, level.upper(), logging.WARN)
    logger.setLevel(level)
    handler = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_DAEMON)
    form = f'{name}: %(message)s'
    if level == logging.DEBUG:
        form += ' %(module)s:%(lineno)d in %(funcName)s()'
    form = logging.Formatter(form)
    handler.setFormatter(form)
    logger.addHandler(handler)
    return logger
