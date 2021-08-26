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
        help='see readme'
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
        help='path to output file - if file exists the new results will be appended'
    )

    return parser
