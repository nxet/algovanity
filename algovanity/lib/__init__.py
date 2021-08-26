from multiprocessing import cpu_count
from multiprocessing import Process, Queue, Value
from time import time, sleep

from algovanity.lib.helpers.mproc import job_worker, job_status, job_terminate, job_update_matches
from algovanity.lib.helpers.patterns import parse_patterns


class AlgoVanity:

    _debug = False
    _logger = None

    _counter_attempts = []
    _queue_matches = []
    _procs = []

    patterns = []
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
                target = job_worker,
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
                self.matches = job_update_matches(self._queue_matches, self.matches, output=output, debug=debug, logger=logger)
                job_status(self._queue_matches, self._counter_attempts, self.matches, self._time_start, debug=debug, logger=logger)
        except KeyboardInterrupt:
            print('') # because `job_status`
            job_terminate(self._procs, debug=debug, logger=logger)
            self.matches = job_update_matches(self._queue_matches, self.matches, output=output, debug=debug, logger=logger)
            job_status(self._queue_matches, self._counter_attempts, self.matches, self._time_start, debug=debug, logger=logger)
            print('') # because `job_status`
        return True


    def load_patterns(self, patterns, debug=None, logger=None):
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        self.patterns = parse_patterns(patterns, debug=debug, logger=logger)
        return True
