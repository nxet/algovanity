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
from multiprocessing import Process
from time import time, sleep

from algovanity.lib.helpers.matches import matches_pull_from_queue
from algovanity.lib.helpers.matches import algo_find_address


def job_init(patterns, queue, counter, procs_max=None, debug=False, logger=None):
    '''
    initialize and start the workers

    Arguments
        `patterns`      <list>      list of patterns to match
        `queue`         <multiprocessing.Queue>
        `counter`       <multiprocessing.Value>
        `procs_max`     <int>       maximum concurrent processes
                                    if omitted defaults to `multiprocessing.cpu_count()`

    Returns
        `procs`         <list>      list of spawned subprocesses
    '''
    procs = []
    if procs_max is None:
        procs_max = cpu_count()
    for i in range(procs_max):
        p = Process(
            target = job_worker,
            args = (patterns, queue, counter, debug, logger),
        )
        p.daemon = True
        p.start()
        procs.append(p)
    if logger:
        logger.info(f'started with {procs_max} subprocesses')
    return procs


def job_main(queue, counter, procs, matches, time_start, output=None, debug=False, logger=None):
    '''
    lock in a loop printing status info every 2s and waiting for termination signals

    Arguments
        `queue`         <multiprocessing.Queue>
        `counter`       <multiprocessing.Value>
        `procs`         <list>
        `matches`       <list>      list of parsed matches
        `time_start`    <float>
        `output`        <str>       path to file where new matches will be appended
    '''
    try:
        while True:
            sleep(2)
            matches = job_update_matches(queue, matches, output=output, debug=debug, logger=logger)
            job_status(queue, counter, matches, time_start, debug=debug, logger=logger)
    except KeyboardInterrupt:
        print('') # because `job_status`
        job_terminate(procs, debug=debug, logger=logger)
        matches = job_update_matches(queue, matches, output=output, debug=debug, logger=logger)
        job_status(queue, counter, matches, time_start, debug=debug, logger=logger)
        print('') # because `job_status`
        if logger:
            logger.info(f'finished, {len(matches)} matches found')
    return True


def job_terminate(procs, debug=False, logger=None):
    '''
    wait for all subprocesses to return and close them

    Arguments
        `procs`     <list>      list of running <multiprocessing.Process> objects
    '''
    for proc in procs:
        if proc.is_alive():
            proc.join()
            proc.close()
    if logger:
        logger.info('terminated')
    return True


def job_status(queue, counter, matches, time_start, debug=False, logger=None):
    '''
    parse operation statistics and print them to console
    NB: this method prints a starting carriage-return and no line break (in order to overwrite the old status in each loop) and therefore requires a final `print('')` call to close the current line and print other data below

    Arguments
        `queue`         <multiprocessing.Queue>
        `counter`       <multiprocessing.Value>
        `matches`       <list>      parsed matches storage
        `time_start`    <float>
    '''
    with counter.get_lock():
        attempts = counter.value
    elapsed = round(time() - time_start)
    results = queue.qsize() + len(matches)
    ats = round(attempts / elapsed)
    print(f'\r{elapsed}s - {results} matches in {attempts} attempts ({ats}/sec)', end='')
    return True


def job_update_matches(queue, matches, output=None, debug=False, logger=None):
    '''
    checks for new matches added to queue, for each available:
        - append to `matches` list
        - append to `output` file
        - print original pattern, address and private key

    Arguments
        `queue`     <multiprocessing.Queue>
        `matches`   <list>      parsed matches storage
        `output`    <str>       path to file where new matches will be appended

    Returns
        `matches`   <list>      updated matches list
    '''
    pulled = matches_pull_from_queue(queue, debug=debug, logger=logger)
    _f = None
    if pulled:
        print('\r', end='') # allows to overwrite status line
        if output is not None:
            try:
                _f = open(output, 'a')
            except FileNotFoundError:
                _f = open(output, 'w')
                if logger:
                    logger.info(f'created output file {output}')
        for match in pulled:
            matches.append(match)
            position, pattern, original, address, private_key = match
            print(original, address, private_key)
            if _f is not None:
                _f.write(f'{original} {address} {private_key}\r\n')
        if _f is not None:
            _f.close()
    return matches


def job_worker(patterns, matches, counter, debug=False, logger=None):
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
            found = algo_find_address(patterns, debug=debug, logger=logger)
            if found:
                for match in found:
                    matches.put(match)
    except KeyboardInterrupt:
        try:
            counter.release()
        except AssertionError as exc:
            if 'attempt to release recursive lock not owned by thread' not in str(exc):
                raise exc
        return
