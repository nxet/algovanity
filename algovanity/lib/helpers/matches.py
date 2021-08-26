from algosdk import account


def matches_pull_from_queue(queue, debug=False, logger=None):
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


def algo_find_address(patterns, debug=False, logger=None):
    private_key, address = account.generate_account()
    for position, pattern, original in patterns:
        if \
            (position == 'start' and address.startswith(pattern)) or \
            (position == 'end' and address.endswith(pattern)) or \
            (position == 'edges' and address.startswith(pattern[0]) and address.endswith(pattern[1])):
            return position, pattern, original, address, private_key
    return None
