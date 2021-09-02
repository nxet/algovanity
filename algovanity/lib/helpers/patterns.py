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

from re import compile as re_compile


regex_patterns_parse = {
    'start': re_compile('^([A-Z2-7]*)\.\.\.$'),
    'end': re_compile('^\.\.\.([A-Z2-7]*)$'),
    'edges': re_compile('^([A-Z2-7]*)\.\.\.([A-Z2-7]*)$'),
}

regex_patterns_match = {
    'start': '^{}[A-Z2-7]*$',
    'end': '^[A-Z2-7]*{}$',
    'edges': '^{}[A-Z2-7]*{}$',
}


def parse_pattern(pattern, debug=False, logger=None):
    '''
    parse a single pattern with regex, returns the matched `position` and `patterns`

    Parsing rules
        `start`     ^([A-Z2-7]*)\.\.\.$                     ADDR...
        `end`       ^\.\.\.([A-Z2-7]*)$                     ...ADDR
        `edges`     ^([A-Z2-7]*)\.\.\.([A-Z2-7]*)$          COOL...ADDR
        `regex`     <str> will use the provided regex string

    Arguments
        `pattern`      <str>       string to parse

    Returns
        `parsed`       <tuple>     (position, patterns)
    '''
    for ii in ('0', '1', '8', '9'):
        if ii in pattern:
            raise ValueError('Valid Algorand addresses can NOT contain the numbers 0, 1, 8 and 9')
    pattern = pattern.upper()
    for pos in regex_patterns_parse:
        parsed = regex_patterns_parse[pos].fullmatch(pattern)
        if parsed:
            matcher = regex_patterns_match[pos].format(*parsed.groups())
            return pos, re_compile(matcher)
    return pos, re_compile(pattern)


def parse_patterns(patterns, debug=False, logger=None):
    '''
    loop over all provided `patterns` and parse them

    Arguments
        `patterns`      <list>      list of pattern strings to parse

    Returns
        `parsed`      <list>        list of parsed pattern strings
    '''
    parsed = []
    for orig in patterns:
        position, matcher = parse_pattern(orig, debug=debug, logger=logger)
        parsed.append((position, matcher, orig, ))
    if logger:
        logger.info(f'loaded {len(parsed)} patterns')
    return parsed
