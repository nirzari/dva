'''
cache and tools
'''

import sys
import logging
import threading
import socket
from ..tools.retrying import retrying
from stitches import Connection, Expect, ExpectFailed
from stitches.connection import StitchesConnectionException

CONNECTION_ATTEMPTS = 120
CONNECTION_ATTEMPTS_RETRY_AFTER = 1
CONNECTION_CACHE = {}

logger = logging.getLogger(__name__)

class ConnectionCacheError(Exception):
    '''bad things happen in connection cache'''

def connection_cache_key(params):
    '''params to connection cache key tuple: (threading.current_thread().ident, host, user, key)'''
    try:
        return threading.current_thread().ident, params['hostname'], params['ssh']['user'], params['ssh']['keyfile']
    except KeyError as err:
        # some key is missing in params
        raise ConnectionCacheError('params missing key: %s' % err)

def drop_connection(params):
    """ Close&remove connection """
    key = connection_cache_key(params)
    try:
        CONNECTION_CACHE.pop(key).disconnect()
        logger.debug('dropped: %s', key)
    except KeyError as err:
        raise ConnectionCacheError('closing a non-existent connection: %s' % (key,))

def assert_connection(connection):
    '''assert a connection is alive; wel... ;) at a point in time'''
    logger.debug('asserting connection: %s', connection)
    Expect.ping_pong(connection, 'uname', 'Linux')
    logger.debug('asserting connection: %s passed', connection) 

@retrying(maxtries=CONNECTION_ATTEMPTS, sleep=CONNECTION_ATTEMPTS_RETRY_AFTER, loglevel=logging.DEBUG,
            final_exception=ConnectionCacheError)
def get_connection(params):
    '''Get connection connection based on params. Retrying.'''
    # maybe the connection is cached...
    key = connection_cache_key(params)
    try:
        connection = CONNECTION_CACHE[key]
        logger.debug('cache hit: %s', key)
    except KeyError as err:
        logger.debug('cache miss: %s', key)
        _, host, user, ssh_key = key
        CONNECTION_CACHE[key] = Connection(host, user, ssh_key)
        logger.debug('got new connection: %s', CONNECTION_CACHE[key])

    try:
        # make sure the connection is alive
        assert_connection(CONNECTION_CACHE[key])
        logger.debug('got alive connection: %s', CONNECTION_CACHE[key])
    except (StitchesConnectionException, ExpectFailed, IOError, socket.error) as err:
        # something went wrong --- drop and keep retrying
        logger.debug('got %s asserting %s', err, CONNECTION_CACHE[key])
        drop_connection(params)
        raise sys.exc_info()

    # got connection --- return
    return CONNECTION_CACHE[key]
