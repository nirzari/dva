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

def print_xunit(data, aname, area):
    agg_data = aggregate.flat(data, area)
    error = 0
    fail = 0
    skip = 0
    total = 0
    testcase = ""
    testsuite = ""
    for name,data in agg_data.items():
        for test in data:
            total += 1
            if test.has_key('test'):
                testcase += '<testcase classname="tests" name="%s.%s">' % (test['test']['stage'],test['test']['name'])
                if test['test']['result'] != 'passed':
                    fail += 1
                    testcase += '<error type="%s"><![CDATA[%s]]></error>' % (test['test']['result'],test['test']['log'])
            else:
                testcase += '<testcase classname="stage" name="%s">' % test['stage_name']
                if test['stage_result'] != 'passed':
                    if test['stage_result'] == 'skip':
                        skip += 1
                    else:
                        error += 1
                    testcase += '<error type="%s"><![CDATA[%s]]></error>' % (test['stage_result'],test['stage_exception'])
            testcase += '</testcase>\n'
    testsuite += '<testsuite name="validation" tests="%d" errors="%d" failures="%d" skip="%d">\n' % (total,error,fail,skip)
    testcase += '</testsuite>\n'
    print('<?xml version="1.0" encoding="UTF-8"?>\n%s%s' % (testsuite,testcase))

def main(config, istream,test_whitelist,compare,xunit):
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
        if xunit:
            print_xunit(data,aname,area)
        else:
            print_failed(data,aname,area,whitelist,area2)
