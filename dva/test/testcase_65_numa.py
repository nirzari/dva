""" This module contains testcase_65_numa test """
from testcase import Testcase


class testcase_65_numa(Testcase):
    """
    Check if NUMA is enabled on machine
    """
    stages = ['stage1', 'stage2']
    tags = ['default', 'kernel']
    applicable = {'virtualization': 'hvm', 'platform': '(?i)BETA|RHEL|ATOMIC', 'version': 'OS (>=6.6)', 'cloudhwname': 'c3.*'}

    # pylint: disable=unused-argument
    def test(self, connection, params):
        """ Perform test"""
        self.get_return_value(connection, 'dmesg | grep "No NUMA configuration found"', 15, 1) #expecting to return 1 - need to do it this way because of different output on different versions of RHEL

        return self.log
