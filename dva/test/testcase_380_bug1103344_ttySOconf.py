""" This module contains testcase_380_bug1103344_ttySOconf.py test """
from testcase import Testcase


class testcase_380_bug1103344_ttySOconf(Testcase):
    """
    Check if ttyS0.conf is moved to .bak file
    """
    stages = ['stage1', 'stage2']
    tags = ['default', 'kernel']
    applicable = {'virtualization': 'hvm', 'platform': '(?i)BETA|RHEL|ATOMIC', 'version': 'OS (>=6.7, <7.0)'}

    # pylint: disable=unused-argument
    def test(self, connection, params):
        """ Perform test"""
        self.get_return_value(connection, 'ls -l /etc/init/ttyS0.conf', 15, 2)
        self.get_return_value(connection, 'ls -l /etc/init/ttyS0.bak')

        return self.log
