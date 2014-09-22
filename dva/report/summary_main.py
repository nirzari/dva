'''
validation summary report function module
'''
import sys
import time
import logging
import bugzilla
import tempfile
import aggregate
from ..tools.retrying import retrying, EAgain
from ..work.data import load_yaml, save_result
from ..work.common import RESULT_PASSED
from result import get_hwp_result
from gevent.pool import Pool
from gevent.coros import RLock
import yaml
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

logger = logging.getLogger(__name__)

def transform(ami, version, arch, region, itype, agg_data):
    for hwp in agg_data:
        print hwp
        sub_result, sub_log = get_hwp_result(agg_data[hwp], False)
        return region, sub_result

def main(config, istream):
    logger.debug('starting generation from file %s',istream)
    data = load_yaml(istream)
    statuses = []
#    agg_data = aggregate.flat(data, 'region', 'version', 'arch', 'itype', 'ami', 'cloudhwname')
    agg_data = aggregate.flat(data, 'cloudhwname')
    for hwname,data in agg_data.items():
        print('HWNAME: %s' % hwname[0])
        for test in data:
            if test.has_key('test'):
                if test['test']['result'] != 'passed':
                    print('   Failed test %s' % test['test']['name'])
#    statuses.append((ami, version, arch, region, itype, agg_data[region][version][arch][itype][ami]))
#    pool = Pool(128)
#    statuses = pool.map(lambda args: transform(*args), statuses)
#    for region, status in statuses:
#        print("Region: %s; Status: %s" % (region,status))
