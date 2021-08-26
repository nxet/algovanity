from multiprocessing import cpu_count
from multiprocessing import Process
from time import time, sleep

from algovanity.lib.helpers.matches import matches_pull_from_queue
from algovanity.lib.helpers.matches import algo_find_address


def job_init(patterns, queue, counter, procs_max=None, debug=False, logger=None):
    '''
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
    return procs


def job_main(queue, counter, procs, matches, time_start, output=None, debug=False, logger=None):
    '''
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
    return True


def job_terminate(procs, debug=False, logger=None):
    for proc in procs:
        if proc.is_alive():
            proc.join()
            proc.close()
    return True


def job_status(queue, counter, matches, time_start, debug=False, logger=None):
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
            match = algo_find_address(patterns, debug=debug, logger=logger)
            if match:
                matches.put(match)
    except KeyboardInterrupt:
        try:
            counter.release()
        except AssertionError as exc:
            if 'attempt to release recursive lock not owned by thread' not in str(exc):
                raise exc
        return
