""" This module contains testcase_99_package_version_check test """
from testcase import Testcase, SkipException
from dva.work.data import load_yaml
import os
import re
import string


class testcase_99_package_version_check(Testcase):
    """
    We're testing here whether a pre-defined set of packages is present.
    This can be useful to see if all packages provided by an errata are
    present, for instance.

    This test requires an external list of packages saved in
    data/packages_generic.yaml
    file, e.g.
    - ipa-python-3.0.0-47.el6_7.2
    - libtalloc-2.1.5-1.el6_7
    - libtdb-1.3.8-1.el6_7
    - libtevent-0.9.26-2.el6_7

    possibly using regular expression:
    - samba-[a-z]+-3.6.23-30.el6_7

    If the above mentioned data file is missing, the test is skipped.
    """
    stages = ['stage0']
    tags = ['default']

    # pylint: disable=W0613
    def test(self, connection, params):
        """ Perform test """

        filename = 'packages_generic.yaml'
        path = os.path.sep.join([self.datadir, filename])
        if not os.path.exists(path):
            raise SkipException('packages list %s not provided, skipping this test' % path)
        else:
            fd = open(path)
            required_packages = load_yaml(fd)
            if not required_packages:
                raise SkipException('package list was not provided in %s, skipping this test' % path)
            else:
                self.log.append({'required_packages': required_packages})

        # we get a full list of packages installed here
        sin, sout, serr = connection.exec_command("rpm -qa")
        packages_result = sout.read()
        packages_list = packages_result.splitlines()

        test_conclusion = True

        for required_package in required_packages:
            p = re.compile(required_package, re.DOTALL)
            search_result = p.search(packages_result)
            if search_result == None:
                test_conclusion = False
                self.log.append({'package NOT found': required_package})
            else:
                self.log.append({'package found': search_result.group()})

        if test_conclusion is False:
            self.log.append({'comment': packages_list})
            self.log.append({'result': 'failed', 'comment': 'Failed to get package set'})
        else:
            self.log.append({'result': 'passed'})
        return self.log
