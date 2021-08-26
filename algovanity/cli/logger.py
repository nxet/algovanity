# algovanity - generate vanity addresses for the Algorand blockchain
# Copyright (C) 2021 nxet <nxet821@protonmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
