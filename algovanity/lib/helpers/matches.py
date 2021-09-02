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

from algosdk import account


def matches_pull_from_queue(queue, debug=False, logger=None):
    '''
    pull all available matches from queue and return a list

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
    '''
    generate a random Algorand (address, private_key) pair and attempt to match it against the provided `patterns`

    Arguments
        `patterns`      <list>      list of patterns to match

    Returns
        `matches`       <list>      list of matches in the form (position, matcher, original, address, private_key)
    '''
    matches = []
    private_key, address = account.generate_account()
    for position, matcher, original in patterns:
        match = matcher.fullmatch(address)
        if match:
            matches.append((position, matcher, original, address, private_key))
            if logger:
                logger.info(f'match found for pattern `{original}`')
    return matches
