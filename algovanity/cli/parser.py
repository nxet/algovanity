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
