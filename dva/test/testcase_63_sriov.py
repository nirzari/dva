""" This module contains testcase_63_sriov test """
from testcase import Testcase


class testcase_63_sriov(Testcase):
    """
    Check various cpu flags
    """
    stages = ['stage1']
    tags = ['default', 'kernel']
    applicable = {'virtualization': 'hvm', 'platform': '(?i)BETA|RHEL|ATOMIC', 'version': 'OS (>=6.6)'}

    # pylint: disable=unused-argument
    def test(self, connection, params):
        """ Perform test """
        self.get_return_value(connection, 'lsmod | grep ixgbevf')

        return self.log
