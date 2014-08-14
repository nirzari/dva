'''
basic data-parallel main function module
'''

import gevent
from gevent import monkey; monkey.patch_all()
from gevent.coros import RLock
from gevent.pool import Pool

import logging
from data import load, save_result, strip_ephemeral
from serial_process import process, required_actions_count, print_progress_info
from serial_main import process, required_actions_count, print_progress_info
logger = logging.getLogger(__name__)

PROCESSED=0
TOTAL=0

REPORT_LOCK = RLock()


def target(ostream, params):
    global PROCESSED, REPORT_LOCK, TOTAL
    for result in process(params):
        with REPORT_LOCK:
            PROCESSED += 1
            print_progress_info(PROCESSED, TOTAL)
            save_result(ostream, strip_ephemeral(result))



def main(conf, istream, ostream, test_whitelist, test_blacklist, stage_whitelist, stage_blacklist, no_action):
    ''' main parallel-data worker function'''
    global TOTAL
    params = dict(test_whitelist=test_whitelist, test_blacklist=test_blacklist,
                    stage_whitelist=stage_whitelist, stage_blacklist=stage_blacklist,
                   enabled=not no_action)
    params = load(istream, config_file=conf, augment=params)
    TOTAL = required_actions_count(params)
    print_progress_info(PROCESSED, TOTAL)
    pool = gevent.pool.Pool(size=32)
    pool.map(lambda item: target(ostream, item), params)

