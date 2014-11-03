'''
tool for uploading data to Jenkins
'''
import sys
import time
import logging
import tempfile
from ..tools.retrying import retrying, EAgain
from ..work.data import load_yaml, save_result
from ..work.common import RESULT_PASSED

logger = logging.getLogger(__name__)

def main(config, istream):
    pass
