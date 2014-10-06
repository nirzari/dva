dva
===

__dva's validation. again.__
* `dva` is a tool to sanity-check image instances in cloud
* this is achieved by executing same test cases over various images and instance types
* expected test results usually depend on OS (minor) version
* primary focus is `RHEL` release validation in [EC2](http://aws.amazon.com/documentation/ec2/)
* `OpenStack` and `Fedora` is supported, too
* 3rd-party test modules are supported

Installation
------------
* `sudo python setup.py install`
* or `sudo pip install dva`

Usage
-----
* dry-run: `dva validate -n < data.yaml > result.yaml`
* `dva validate < data.yaml > result.yaml`
* `dva bugzilla < result.yaml > buglist.yaml`
* `# dva result < result.yaml > result.txt`
* for complete options list: `dva --help`
* for failure summary use: `dva summary -i result.yaml`
* simulate valid execution: `dva validate -i data.yaml --parallel-tests=1 --sorted-mode`
* load custom tests: `dva validate < data.yaml > result.yaml --test-modules=my.tests`

Notes
-----
* please bare in mind the limit of opened file-descriptors is usualy 1024
* `--parallel-tests` and `--parallel-instances` multiply the usage of file-descriptors needed
* `sshd` puts a limit on the number of sessions users may open in parallel
* usually `--parallel-tests=10` is the maximum possible
* `dva` runs in a single process in [gevent](http://www.gevent.org/) pools
* consider running multiple `dva` instances for large inputs
* not-setting `--sorted-mode` has the benefit of breaking waves in test execution
* for the same reason, image instantiation is randomized through cloud regions

See also
--------
* [wiki](https://github.com/RedHatQE/dva/wiki)
* [valid](https://github.com/RedHatQE/valid)
