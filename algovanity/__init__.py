from multiprocessing import cpu_count
from multiprocessing import Process, Queue, Value
from time import time, sleep
from re import compile as re_compile
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

    def run(self, output=None, procs_max=None, debug=None, logger=None):
        '''
        start the subprocesses and lock in a loop which prints status info every 2s

        Arguments
            `output`        <str>   path to file where new matches will be appended
            `procs_max`     <int>   number of subprocesses to spawn, defaults to `self.procs_max`
        '''
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        self.matches = []
        self._time_start = time()
        procs_max = procs_max if procs_max is not None else self.procs_max
        for i in range(procs_max):
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
                self._job_update_matches(output=output, debug=debug, logger=logger)
                self._job_status(debug=debug, logger=logger)
        except KeyboardInterrupt:
            print('') # because `_job_status`
            self._job_terminate(debug=debug, logger=logger)
            self._job_update_matches(output=output, debug=debug, logger=logger)
            self._job_status(debug=debug, logger=logger)
            print('') # because `_job_status`
        return True

    def _job_terminate(self, debug=None, logger=None):
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        for proc in self._procs:
            if proc.is_alive():
                proc.join()
                proc.close()
        return True

    def _job_status(self, debug=None, logger=None):
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        with self._counter_attempts.get_lock():
            attempts = self._counter_attempts.value
        elapsed = round(time() - self._time_start)
        results = self._queue_matches.qsize() + len(self.matches)
        ats = round(attempts / elapsed)
        print(f'\r{elapsed}s - {results} matches in {attempts} attempts ({ats}/sec)', end='')
        return True

    def _job_update_matches(self, output=None, debug=None, logger=None):
        '''
        checks for new matches added to queue, for each available:
            - add to `self.matches`
            - append to `output` file
            - print original pattern, address and private key

        Arguments
            `output`    <str>   path to file where new matches will be appended
        '''
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
                position, pattern, original, address, private_key = match
                print(original, address, private_key)
                if _f is not None:
                    _f.write(f'{original} {address} {private_key}\r\n')
            if _f is not None:
                _f.close()
        return True

    @classmethod
    def _matches_pull_from_queue(cls, queue, debug=False, logger=None):
        '''
        pulls all available matches from queue and returns a list

        Arguments
            `queue`     <multiprocessing.Queue>     object used by subprocesses to store matches

        Returns
            `matches`   <list>      list of tuples containing (position, pattern, original, address, private_key)
        '''
        matches = []
        while not queue.empty():
            match = queue.get()
            matches.append(match)
        return matches


    def load_patterns(self, patterns, debug=None, logger=None):
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        self.patterns = []
        for orig in patterns:
            position, ptn = self.parse_pattern(orig, debug=debug, logger=logger)
            self.patterns.append((position, ptn, orig, ))
        return True

    _regex_patterns = {
        'start': re_compile('^([a-zA-Z0-9]*)\,start$'),
        'end': re_compile('^([a-zA-Z0-9]*)\,end$'),
        'edges': re_compile('^([a-zA-Z0-9]*)\.\.\.([a-zA-Z0-9]*)$'),
    }

    @classmethod
    def parse_pattern(cls, pattern, debug=False, logger=None):
        out = None
        for pos in cls._regex_patterns:
            match = cls._regex_patterns[pos].fullmatch(pattern)
            if match:
                return pos, match.groups()
        raise ValueError(f'Unable to parse pattern `{pattern}`')


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
            try:
                counter.release()
            except AssertionError as exc:
                if 'attempt to release recursive lock not owned by thread' not in str(exc):
                    raise exc
            return

    @staticmethod
    def find_address(patterns, debug=False, logger=None):
        private_key, address = account.generate_account()
        for position, pattern, original in patterns:
            if \
                (position == 'start' and address.startswith(pattern)) or \
                (position == 'end' and address.endswith(pattern)) or \
                (position == 'edges' and address.startswith(pattern[0]) and address.endswith(pattern[1])):
                return position, pattern, original, address, private_key
        return None
