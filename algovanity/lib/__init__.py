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

from multiprocessing import cpu_count
from multiprocessing import Queue, Value
from time import time

from algovanity.lib.helpers.mproc import job_init, job_main
from algovanity.lib.helpers.patterns import parse_patterns
from algovanity.__metadata__ import __version__


class AlgoVanity:

    __version__ = __version__

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
        self._procs = job_init(self.patterns, self._queue_matches, self._counter_attempts, procs_max, debug=debug, logger=logger)
        if job_main(self._queue_matches, self._counter_attempts, self._procs, self.matches, self._time_start, output, debug=debug, logger=logger):
            return self.matches


    def load_patterns(self, patterns, debug=None, logger=None):
        debug = debug if debug is not None else self._debug
        logger = logger if logger is not None else self._logger
        self.patterns = parse_patterns(patterns, debug=debug, logger=logger)
        return True
