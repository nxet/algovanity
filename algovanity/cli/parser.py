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

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from multiprocessing import cpu_count


def get_parser(name, version):
    parser = ArgumentParser(name, formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'v{version}'
    )
    parser.add_argument(
        '--loglevel',
        type=str,
        choices=['debug', 'info', 'warn', 'error'],
        dest='LOGLEVEL',
        default='info'
    )
    parser.add_argument(
        '--debug',
        const=True,
        dest='DEBUG',
        action='store_const',
        default=False
    )

    parser.add_argument(
        'PATTERNS',
        type=str,
        nargs='+',
        help='''multiple space-separated patterns to match
Supports matching at `start`, `end` and `edges` of
the address, with patterns respectively like `ADDR...`,
`...ADDR` and `COOL...ADDR`.
Alternatively the user can pass a pure regex string
which will be compiled and used to `re.fullmatch`
against generated addresses.
For more details please refer to the README.md file'''
    )
    parser.add_argument(
        '-p', '--procs-max', dest='PROCS_MAX',
        type=int,
        default=cpu_count(),
        help='maximum amount of concurrent processes to run, defaults to CPU number'
    )
    parser.add_argument(
        '-o', '--output', dest='OUTPUT',
        type=str,
        help='optional path to output file - if file exists the new results will be appended'
    )

    return parser
