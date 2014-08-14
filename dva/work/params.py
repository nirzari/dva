'''
params handling stuff
'''

def when_enabled(fn):
    '''
    enabled-params check decorator; if not enabled; just return the params
    '''
    from data import DataError
    def wrapper(params):
        try:
            enabled = params['enabled']
        except KeyError as err:
            raise DataError('params misses %s' % err)
        if not enabled:
            return params
        return fn(params)
    return wrapper



