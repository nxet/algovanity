from algosdk import account


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


    @staticmethod
    def _job_find_address(DONE, patterns, matches, counter, debug=False, logger=None):
        '''
        Arguments
            `DONE`      <bool>      flag to read at each loop
            `patterns`  <list>      list of patterns to match, see config
            `matches`   <multiprocessing.Queue>
            `counter`   <multiprocessing.Value>
        '''
        while not DONE:
            with counter.get_lock():
                counter.value += 1
            match = AlgoVanity.find_address(patterns, debug=debug, logger=logger)
            if match:
                matches.put(match)

    @staticmethod
    def find_address(patterns, debug=False, logger=None):
        private_key, address = account.generate_account()
        for pattern, position in patterns:
            if (position == 'start' and address.startswith(pattern)) or (position == 'end' and address.endswith(pattern)):
                return pattern, position, address, private_key
        return None
