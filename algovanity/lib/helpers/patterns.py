from re import compile as re_compile


regex_patterns_parse = {
    'start': re_compile('^([A-Z0-9]*)\.\.\.$'),
    'end': re_compile('^\.\.\.([A-Z0-9]*)$'),
    'edges': re_compile('^([A-Z0-9]*)\.\.\.([A-Z0-9]*)$'),
}

regex_patterns_match = {
    'start': '^{}[A-Z0-9]*$',
    'end': '^[A-Z0-9]*{}$',
    'edges': '^{}[A-Z0-9]*{}$',
}


def parse_pattern(pattern, debug=False, logger=None):
    '''
    parse a single pattern with regex, returns the matched `position` and `patterns`

    Parsing rules
        `start`     ^([A-Z0-9]*)\.\.\.$                     ADDR...
        `end`       ^\.\.\.([A-Z0-9]*)$                     ...ADDR
        `edges`     ^([A-Z0-9]*)\.\.\.([A-Z0-9]*)$          COOL...ADDR
        `regex`     <str> will use the provided regex string

    Arguments
        `pattern`      <str>       string to parse

    Returns
        `parsed`       <tuple>     (position, patterns)
    '''
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
    return parsed
