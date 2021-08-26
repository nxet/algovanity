from re import compile as re_compile


regex_patterns = {
    'start': re_compile('^([A-Z0-9]*)\,START$'),
    'end': re_compile('^([A-Z0-9]*)\,END$'),
    'edges': re_compile('^([A-Z0-9]*)\.\.\.([A-Z0-9]*)$'),
}

def parse_pattern(cls, pattern, debug=False, logger=None):
    out = None
    pattern = pattern.upper()
    for pos in regex_patterns:
        match = regex_patterns[pos].fullmatch(pattern)
        if match:
            return pos, match.groups()
    raise ValueError(f'Unable to parse pattern `{pattern}`')

def parse_patterns(patterns, debug=None, logger=None):
    patterns = []
    for orig in patterns:
        position, ptn = parse_pattern(orig, debug=debug, logger=logger)
        patterns.append((position, ptn, orig, ))
    return patterns
