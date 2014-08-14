'''
connection ctx manager module
'''

import stitches
import contextlib


@contextlib.contextmanager
def connection(host, user, key):
    '''ctx manager for connections'''
    connection = stitches.Connection(host, user, key)
    try:
        yield connection
    finally:
        connection.disconnect()


