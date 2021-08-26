#!/usr/bin/env python3

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
