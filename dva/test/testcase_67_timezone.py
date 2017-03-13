""" This module contains  67_timezone test - bz1187669 """
from testcase import Testcase


class testcase_67_timezone(Testcase):
    """
    Check that the default timezone is set to UTC
    """
    stages = ['stage1']
    tags = ['default']
    applicable = {'virtualization': 'hvm', 'platform': '(?i)BETA|RHEL', 'version': 'OS (>6.8, >7.2)'}

    # pylint: disable=unused-argument
    def test(self, connection, params):
        self.get_return_value(connection, 'date -u | grep UTC')
        return self.log

