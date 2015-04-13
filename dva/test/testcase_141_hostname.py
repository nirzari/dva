""" This module contains  testcase_141_hostname test """
from testcase import Testcase


class testcase_141_hostname(Testcase):
    """
    Check that reboot doesn't change the hostname
    """
    stages = ['stage1', 'stage2']
    tags = ['default']
    applicable = {'virtualization': 'hvm', 'platform': '(?i)BETA|RHEL|ATOMIC', 'version': 'OS (>=6.8)'}

    # pylint: disable=unused-argument
    def test(self, connection, params):
        """ Check that reboot doesn't change the hostname """
        """ 1. Check if the file with a hostname exists, otherwise create such a file. """  
        self.get_return_value(connection, 'test -f /root/hostname_text.txt || hostname > /root/hostname_text.txt; sync') 
        """ If it's the first stage, it will grep the hostname from the file which was created with the previous command. If it's the second stage, it will check that the current hostname matches the hostname written in the file before reboot. """
        self.get_return_value(connection, 'grep -x `hostname` /root/hostname_text.txt')
        return self.log

