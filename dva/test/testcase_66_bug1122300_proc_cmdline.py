""" This module contains  testcase_66_bug1122300_proc_cmdline test """
from testcase import Testcase


class testcase_66_bug1122300_proc_cmdline(Testcase):
    """
    Check various grub parameters
    """
    stages = ['stage1', 'stage2']
    tags = ['default', 'kernel']
    applicable = {'virtualization': 'hvm', 'platform': '(?i)BETA|RHEL|ATOMIC', 'version': 'OS (>=6.6)'}

    # pylint: disable=unused-argument
    def test(self, connection, params):
        """ Perform test of bug 1122300"""
        self.get_return_value(connection, 'cat /proc/cmdline | grep -v -i quiet')
        self.get_return_value(connection, 'cat /proc/cmdline | grep -v -i rhgb')

        return self.log
