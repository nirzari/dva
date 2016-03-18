""" This module contains testcase_09_nameserver test """
from testcase import Testcase


class testcase_09_nameserver(Testcase):
    """
    Check if DNS resolving works
    """
    stages = ['stage1']
    tags = ['default']

    def test(self, connection, params):
        """ Perform test """

        prod = params['platform'].upper()
        ver = params['version']
        self.get_return_value(connection, 'ping -c 5 google-public-dns-a.google.com | grep 8.8.8.8', 30)
        return self.log
