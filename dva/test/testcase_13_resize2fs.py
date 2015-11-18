""" This module contains testcase_13_resize2fs test """
from testcase import Testcase


class testcase_13_resize2fs(Testcase):
    """
    The instances are always created with a 15GB root device (unlike
    the AWS default of 8GB. The point is whether we're able to allocate
    the space. Please note that cloud-init does the resize automatically.
    """
    stages = ['stage1']
    applicable = {'platform': '(?i)RHEL|BETA|ATOMIC', 'version': 'OS (>=5.5, >=6.7, >=7.1)'}
    tags = ['default']

    def test(self, connection, params):
        """ Perform test """

        plat = params['platform'].upper()
        prod = params['product'].upper()
        ver = params['version']
        if self.get_return_value(connection, 'rpm -q cloud-init', nolog=True) == 1:
            # cloud-init not installed, resize
            if plat in ['RHEL', 'BETA'] and ver.startswith('6.'):
                self.get_return_value(connection, 'if [ -b /dev/xvde1 ]; then resize2fs -p /dev/xvde1 15000M ; else resize2fs -p /dev/xvda1 15000M; fi', 180)
            elif plat in ['RHEL', 'BETA'] and ver.startswith('5.'):
                self.get_return_value(connection, 'resize2fs -p /dev/sda1 15000M', 180)
        # in case of atomic, we look at the size of the volume group
        if prod == 'ATOMIC':
            self.get_return_value(connection, 'vgs | grep "14\.[0-9]\{2\}g"')
        else:
            self.get_return_value(connection, 'df -h | grep 15G')
        return self.log
