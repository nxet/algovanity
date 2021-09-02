#!/usr/bin/env python3

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

from algovanity.lib import AlgoVanity
from algovanity.__metadata__ import __pkgname__, __version__
from algovanity.cli.parser import get_parser
from algovanity.cli.logger import get_logger


def main():
    parser = get_parser(__pkgname__, __version__)
    args = parser.parse_args()
    logger = get_logger(__pkgname__, args.LOGLEVEL)
    client = AlgoVanity(patterns=args.PATTERNS, procs_max=args.PROCS_MAX, debug=args.DEBUG, logger=logger)
    client.run(output=args.OUTPUT)


if __name__ == '__main__':
    main()
