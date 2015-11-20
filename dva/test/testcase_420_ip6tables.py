""" This module contains testcase_420_ip6tables test - bz1030586 """
from testcase import Testcase


class testcase_420_ip6tables(Testcase):
    """
    Check that ip6tables is disabled by default
    """
    stages = ['stage1']
    tags = ['default']
    applicable = {'virtualization': 'hvm', 'platform': '(?i)BETA|RHEL', 'version': 'OS (>=6.8, <7.0)'}

    def test(self, connection, params):
        self.get_return_value(connection, 'chkconfig --list ip6tables | grep \'0:off[[:space:]]*1:off[[:space:]]*2:off[[:space:]]*3:off[[:space:]]*4:off[[:space:]]*5:off[[:space:]]*6:off\'')
        return self.log
