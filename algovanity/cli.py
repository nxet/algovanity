#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from multiprocessing import cpu_count

from algovanity import AlgoVanity
from algovanity.__metadata__ import __pkgname__, __version__


def main():
    parser = ArgumentParser(__pkgname__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('PATTERNS', type=str, nargs='+', help='see readme')
    parser.add_argument('-p', '--procs-max', dest='PROCS_MAX', type=int, default=cpu_count(), help='maximum amount of concurrent processes to run, defaults to CPU number')
    parser.add_argument('-o', '--output', dest='OUTPUT', type=str, help='path to output file - if file exists the new results will be appended')
    parser.add_argument('--debug', const=True, dest='DEBUG', action='store_const', default=False)
    args = parser.parse_args()
    logger = None #get_logger(__pkgname__, args.LOGLEVEL)
    client = AlgoVanity(patterns=args.PATTERNS, procs_max=args.PROCS_MAX, debug=args.DEBUG, logger=logger)
    client.run(output=args.OUTPUT)
    from pprint import pprint; pprint(client.matches)


if __name__ == '__main__':
    main()
