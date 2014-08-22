'''
the test execution module
'''


import sys
import logging
import traceback
from stitches import Expect, ExpectFailed
from stitches.connection import StitchesConnectionException
from ..tools.registry import TEST_CLASSES, TEST_STAGES
from ..tools.logged import logged
from ..connection.cache import get_connection, assert_connection, connection_cache_key, drop_connection, ConnectionCacheError
from data import brief
from params import when_enabled
from common import RESULT_ERROR, RESULT_PASSED, RESULT_FAILED


logger = logging.getLogger(__name__)

class TestingError(Exception):
    '''Some testing issue appeared'''

@when_enabled
def test_execute(params):
    """
    Testing stage: perform all tests required in params
    @param params: testing parameters
    @type params: dict
    @return: list of test results
    """
    assert 'test' in params, 'test field missing in %s' % brief(params)
    assert 'name' in params['test'], 'test name field missing in %s' % brief(params)
    assert 'stage' in params['test'], 'test stage field missing in %s' % brief(params)
    test_name = params['test']['name']
    test_stage = params['test']['stage']
    params['test']['exception'] = None
    params['test']['log'] = []
    params['test']['result'] = RESULT_PASSED
    hostname = params['hostname']

    logger.debug('trying %s %s %s', hostname, test_stage, test_name)
    try:
        test_cls = TEST_CLASSES[test_name]
        stage = TEST_STAGES[test_stage]
        assert test_name in stage, 'could not locate test %s in stage %s' % (test_name, test_stage)
    except KeyError as err:
        params['test_result'] = 'error: missing test/stage: %s/%s' % (test_name, test_stage)
        raise TestingError('missing test: %' % test_name)

    # cached connection; tries reconnecting
    con = get_connection(params)

    # perform the testing
    try:
        test_obj = test_cls()
        test_obj.test(con, params)
        logger.debug('%s %s %s succeeded', hostname, test_stage, test_name)
    except AssertionError as err:
        # not caught in the test case but means the test failed
        params['test']['result'] = RESULT_FAILED
        params['test']['exception'] = traceback.format_exc()
    else:
        # no assertion errors detected --- check all cmd logs
        test_cmd_results = [cmd['result'] for cmd in test_obj.log if 'result' in cmd]
        test_result = RESULT_ERROR in test_cmd_results and RESULT_ERROR or RESULT_PASSED
        test_result = RESULT_FAILED in test_cmd_results and RESULT_FAILED or RESULT_PASSED
        params['test']['result'] = test_result
    finally:
        params['test']['log'] = test_obj.log
    return params


def execute_tests(original_params):
    '''perform all tests'''
    original_params['stage_name'] = 'execute_tests'
    for stage_name in sorted(original_params['test_stages']):
        for test_name in sorted(original_params['test_stages'][stage_name]):
            params = original_params.copy()
            params['test'] = {
                'name': test_name,
                'stage': stage_name
            }
            params = test_execute(params)
            yield params

