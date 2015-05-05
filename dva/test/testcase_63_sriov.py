""" This module contains testcase_63_sriov test """
from testcase import Testcase, SkipException
SRIOV_INSTANCES = {
     'c4.large',
     'c4.xlarge',
     'c4.2xlarge',
     'c4.4xlarge',
     'c4.8xlarge',
     'c3.large',
     'c3.xlarge',
     'c3.2xlarge',
     'c3.4xlarge',
     'c3.8xlarge',
     'd2.xlarge',
     'd2.2xlarge',
     'd2.4xlarge',
     'd2.8xlarge',
     'i2.xlarge',
     'i2.2xlarge',
     'i2.4xlarge',
     'i2.8xlarge',
     'r3.large',
     'r3.xlarge',
     'r3.2xlarge',
     'r3.4xlarge',
     'r3.8xlarge',
}

class testcase_63_sriov(Testcase):
    """
    Check enhanced networking feature is enabled
    """
    stages = ['stage1']
    tags = ['default', 'kernel']
    applicable = {
        'virtualization': 'hvm',
        'platform': '(?i)BETA|RHEL|ATOMIC',
        'version': 'OS (>=6.6, !=7.0, !=7.1)',
        'cloud': 'ec2',
    }

    # pylint: disable=unused-argument
    def test(self, connection, params):
        """ Perform test """
        if params['cloudhwname'] not in SRIOV_INSTANCES:
            raise SkipException('unsupported instance HW type: %s' % params['cloudhwname'])
        # fetch device driver information
        result = self.get_result(connection, 'ethtool -i eth0 | grep driver')
        assert result.strip() == 'driver: ixgbevf', 'got non-sriov driver: %s' % result

        return self.log
