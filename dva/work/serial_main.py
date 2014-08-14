'''
basic serial main function module
'''

import time
import logging
import traceback
from stage import create_instance, attempt_ssh, allow_root_login, global_setup_script, terminate_instance
from test import execute_tests 
from common import RESULT_ERROR
from data import load, save_result, strip_ephemeral
from stage import STAGES, StageError

logger = logging.getLogger(__name__)

def process(params):
    '''process required acctions'''
    terminate = False
    try:
        params = create_instance(params)
        terminate = True
        yield params
        params = attempt_ssh(params)
        yield params
        params = allow_root_login(params)
        yield params
        params = global_setup_script(params)
        yield params
        for test_result in execute_tests(params):
            yield test_result
    except StageError as err:
        logger.debug('encountered stage error: %s', err)
        yield params
    except Exception as err:
        # unhandled error
        logger.error('unhandled exception: %s', err)
        params['stage_exception'] = traceback.format_exc()
        params['stage_result'] = RESULT_ERROR
        yield params
    finally:
        if terminate:
            yield terminate_instance(params)
   
def required_actions_count(params):
    total = 0
    for item in params:
        total += len(STAGES)
        for test_stage in item['test_stages']:
            for test_name in item['test_stages'][test_stage]:
                total += 1
    return total

def print_progress_info(actual, total):
    '''print progress info actual/total'''
    print '# %s %2.2f%% (%s/%s)' % (time.ctime(), float(actual * 100)/total, actual, total)

def main(conf, istream, ostream, test_whitelist, test_blacklist, stage_whitelist, stage_blacklist, no_action):
    '''
    main worker function
    performs particular stages handling
    generates particular stage/test result list
    '''
    params = dict(test_whitelist=test_whitelist, test_blacklist=test_blacklist,
                    stage_whitelist=stage_whitelist, stage_blacklist=stage_blacklist,
                   enabled=not no_action)
    params = load(istream, config_file=conf, augment=params)
    total = required_actions_count(params)
    processed = 0
    print_progress_info(processed, total)
    for item in params:
        for result in process(item):
            processed += 1 
            save_result(ostream, strip_ephemeral(result))
            print_progress_info(processed, total)

