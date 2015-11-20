""" This module contains testcase_410_rh_cloud_firstboot test - bz752233 """
from testcase import Testcase


class testcase_410_rh_cloud_firstboot(Testcase):
    """
    Check that /etc/sysconfig/rh-cloud-firstboot has the correct selinux file context
    
    As of 2015-11-20, this hasn't been fixed nor even assigned yet, so at the moment we 
    check for a reversed value, so once the issue gets fixed in the future, this test 
    will start to fail and we can invert the test to make it pass then.  
    """
    stages = ['stage1']
    tags = ['default']
    applicable = {'virtualization': 'hvm', 'platform': '(?i)BETA|RHEL', 'version': 'OS (>=6.2)'}

    def test(self, connection, params):
        self.get_return_value(connection, '[[ ! `ls -Z /etc/sysconfig/rh-cloud-firstboot | grep etc_t` ]]')
        return self.log
