
class AlgoVanity:

    _debug = False
    _logger = None

    patterns = None

    def __init__(self, patterns, debug=None, logger=None):
        self._debug = debug if debug is not None else self._debug
        self._logger = logger if logger is not None else self._logger
        self.load_patterns(patterns)

    def load_patterns(self, patterns, debug=None, logger=None):
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        self.patterns = []
        for ptn in patterns:
            ptn,position = self.parse_pattern(ptn, debug=debug, logger=logger)
            self.patterns.append((ptn,position))
        return True

    @classmethod
    def parse_pattern(cls, pattern, debug=False, logger=None):
        position = 'start'
        pattern = pattern.split(',')
        try:
            pattern, position = pattern
            position = position.lower()
        except ValueError as exc:
            if 'not enough values to unpack (expected 2, got' not in str(exc):
                raise exc
            pattern = pattern[0]
        if position not in ('start', 'end'):
            raise ValueError(f'`position` must be one of `start` or `end`, not `{position}`')
        return pattern, position
