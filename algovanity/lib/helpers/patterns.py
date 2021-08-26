from re import compile as re_compile


regex_patterns = {
    'start': re_compile('^([A-Z0-9]*)\,START$'),
    'end': re_compile('^([A-Z0-9]*)\,END$'),
    'edges': re_compile('^([A-Z0-9]*)\.\.\.([A-Z0-9]*)$'),
}

def parse_pattern(pattern, debug=False, logger=None):
    '''
    parse a single pattern with regex, returns the matched `position` and `patterns`

    Parsing rules
        `start`     ^([A-Z0-9]*)\,START$
        `end`       ^([A-Z0-9]*)\,END$
        `edges`     ^([A-Z0-9]*)\.\.\.([A-Z0-9]*)$

    Arguments
        `pattern`      <str>       string to parse

    Returns
        `parsed`       <tuple>     (position, patterns)
    '''
    pattern = pattern.upper()
    for pos in regex_patterns:
        match = regex_patterns[pos].fullmatch(pattern)
        if match:
            return pos, match.groups()
    raise ValueError(f'Unable to parse pattern `{pattern}`')

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
        position, ptn = parse_pattern(orig, debug=debug, logger=logger)
        parsed.append((position, ptn, orig, ))
    return parsed
