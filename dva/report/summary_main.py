'''
validation summary report function module
'''
import sys
import time
import logging
import bugzilla
import tempfile
import aggregate
from html import HTML
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

def print_failed(data, aname, area, whitelist,area2='cloudhwname'):
    agg_data = aggregate.flat(data, area)
    for name,data in agg_data.items():
        print('%s %s' % (aname, name[0]))
        for test in data:
            if test.has_key('test'):
                if test['test']['result'] != 'passed':
                    if test['test']['name'] not in whitelist:
                        print('   Failed test %s (%s)' % (test['test']['name'],test[area2]))
            else:
                if test['stage_result'] == 'skip':
                    print('!! Skipped - most likely unsupported instance type in region. (%s)' % test[area2])
                elif test['stage_result'] != 'passed':
                    print('!! Failed stage %s (%s)' % (test['stage_name'],test[area2]))

def print_failed_html(data, aname, area, whitelist,area2='cloudhwname'):
    agg_data = aggregate.flat(data, area)
    h = HTML('html')
    t = h.table(border='1')
    for name,data in agg_data.items():
        r = t.tr
        r.td(name[0])
        for test in data:
            if test.has_key('test'):
                if test['test']['name'] not in whitelist:
                    testname=test['test']['name']
                    if test['test']['result'] != 'passed':
                        color='red'
                    else:
                        color='green'
                        testname='OK'
                    r.td(testname,bgcolor=color)
    print t

def main(config, istream,test_whitelist,compare,html):
    logger.debug('starting generation from file %s',istream)
    data = load_yaml(istream)
    comparelist = [str(item) for item in compare[0].split(',')]
    whitelist = [str(item) for item in test_whitelist[0].split(',')]
    for area in comparelist:
        area2 = 'cloudhwname'
        if area == 'cloudhwname':
            aname = 'HWNAME:'
            area2 = 'ami'
        elif area == 'region':
            aname = 'REGION:'
        else:
            area = 'ami'
            aname = 'AMI:'
        if html:
            print_failed_html(data,aname,area,whitelist,area2)
        else:
            print_failed(data,aname,area,whitelist,area2)
