""" This module contains testcase_64_blkfront test """
from testcase import Testcase


class testcase_64_blkfront(Testcase):
    """
    Check various cpu flags
    """
    stages = ['stage1']
    tags = ['default', 'kernel']
    applicable = {'virtualization': 'hvm', 'platform': '(?i)BETA|RHEL|ATOMIC', 'version': 'OS (>=6.7)', 'cloudhwname': 'i2.*'}

    # pylint: disable=unused-argument
    def test(self, connection, params):
        """ Perform test of bug 1202393"""
        self.get_return_value(connection, 'dmesg | grep blkfront')
        self.get_return_value(connection, 'dmesg | grep blkfront | grep "persistent grants: enabled; indirect descriptors: disabled"')

        return self.log
