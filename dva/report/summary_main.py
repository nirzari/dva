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


def main(istream):
    logger.debug('starting generation from file %s',istream)
    data = load_yaml(istream)
    agg_data = aggregate.apply(data, 'region', 'version', 'arch', 'itype', 'ami', 'cloudhwname')
