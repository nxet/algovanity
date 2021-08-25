from multiprocessing import cpu_count
from multiprocessing import Process, Queue, Value
from time import time, sleep
from algosdk import account


class AlgoVanity:

    _debug = False
    _logger = None

    _counter_attempts = []
    _queue_matches = []
    _procs = []

    patterns = None
    procs_max = 1

    matches = []

    def __init__(self, patterns, procs_max=None, debug=None, logger=None):
        self._debug = debug if debug is not None else self._debug
        self._logger = logger if logger is not None else self._logger
        self.load_patterns(patterns)
        if procs_max is not None:
            self.procs_max = procs_max
        else:
            self.procs_max = cpu_count()
        self._counter_attempts = Value('i', 0)
        self._queue_matches = Queue()
        self._procs = []

    def run(self, output=None, debug=None, logger=None):
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        self.matches = []
        self._time_start = time()
        for i in range(self.procs_max):
            p = Process(
                target = self._job_worker,
                args = (
                    self.patterns,
                    self._queue_matches,
                    self._counter_attempts,
                    self._debug, self._logger,
                ),
            )
            p.daemon = True
            p.start()
            self._procs.append(p)
        try:
            while True:
                sleep(2)
                # check for new matches, if available print them
                self.update_matches(output=output, debug=debug, logger=logger)
                # print status line
                with self._counter_attempts.get_lock():
                    attempts = self._counter_attempts.value
                elapsed = round(time() - self._time_start)
                results = self._queue_matches.qsize() + len(self.matches)
                ats = round(attempts / elapsed)
                print(f'\r{elapsed}s - {results} matches in {attempts} attempts ({ats}/sec)', end='')
        except KeyboardInterrupt:
            print('')
            self._job_terminate(debug=debug, logger=logger)
            self.update_matches(output=output, debug=debug, logger=logger)

    def _job_terminate(self, debug=None, logger=None):
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        for proc in self._procs:
            if proc.is_alive():
                proc.terminate()
        return True

    def update_matches(self, output=None, debug=None, logger=None):
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        matches = self._matches_pull_from_queue(self._queue_matches, debug=debug, logger=logger)
        _f = None
        if matches:
            print('\r', end='') # allows to overwrite status line
            if output is not None:
                try:
                    _f = open(output, 'a')
                except FileNotFoundError:
                    _f = open(output, 'w')
            for match in matches:
                self.matches.append(match)
                print(*match) # pattern, position, address, pk
                if _f is not None:
                    _f.write(' '.join(match) + '\r\n')
            if _f is not None:
                _f.close()

    @classmethod
    def _matches_pull_from_queue(cls, queue, debug=False, logger=None):
        matches = []
        while not queue.empty():
            match = queue.get()
            matches.append(match)
        return matches


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
    def _job_worker(patterns, matches, counter, debug=False, logger=None):
        '''
        Arguments
            `patterns`  <list>      list of patterns to match, see config
            `matches`   <multiprocessing.Queue>
            `counter`   <multiprocessing.Value>
        '''
        try:
            while True:
                with counter.get_lock():
                    counter.value += 1
                match = AlgoVanity.find_address(patterns, debug=debug, logger=logger)
                if match:
                    matches.put(match)
        except KeyboardInterrupt:
            return

    @staticmethod
    def find_address(patterns, debug=False, logger=None):
        private_key, address = account.generate_account()
        for pattern, position in patterns:
            if (position == 'start' and address.startswith(pattern)) or (position == 'end' and address.endswith(pattern)):
                return pattern, position, address, private_key
        return None
