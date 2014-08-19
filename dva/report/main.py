'''
the main report function module
'''
import logging
from ..work.data import load_yaml
from ..work.common import RESULT_PASSED
from result import get_overall_result

logger = logging.getLogger(__name__)

def main(config, istream, ostream, verbose):
    result, ami_results = get_overall_result(load_yaml(istream), verbose)
    print >>ostream, '# overal result: %s' % result
    for ami_result, ami_log in ami_results:
        print >>ostream, ami_log
    return result == RESULT_PASSED and 0 or 1

