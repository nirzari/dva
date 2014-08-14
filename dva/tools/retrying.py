'''
the retrying callable decorator
'''
import logging
import sys
from functools import wraps
logger = logging.getLogger(__name__)

def retrying(maxtries=3, sleep=10, loglevel=logging.WARNING, final_exception=None):
    '''
    retrying-logic decorator
    @param maxtries: how many times before giving up
    @param sleep: how long to wait between retries
    @param loglevel: at which level to report retries
    @param final_exception: what exception breaks the retries immediately
                            same is risen when too many attempts were hit
    '''
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kvs):
            import time
            import traceback
            ntries = 0
            err = None
            while ntries < maxtries:
                ntries += 1
                logger.debug('%s: try: #%s', fn.__name__, ntries)
                try:
                    return fn(*args, **kvs)
                except final_exception as err:
                    raise type(err)('%s: (try #%s): final_exception: %s' % (fn.__name__, ntries, err))
                except (NameError, TypeError, ValueError, KeyError, IndexError, AttributeError,
                            UnboundLocalError, AssertionError) as err:
                    # too generic exception --- just break
                    logger.error('%s encountered: %s\n%s' % (fn.__name__, err, traceback.format_exc()))
                    raise sys.exc_info()
                except Exception as err:
                    logger.log(loglevel, '%s: (try #%s): %s --- retrying in %ss', fn.__name__, ntries, err, sleep)
                time.sleep(sleep)
            # not reached in case fn call was successful --- return statement
            else:
                raise final_exception('%s: %s. Too many retries: %s.' % (fn.__name__, err, ntries))
        return wrapper
    return decorator


__all__ = ['retrying']
