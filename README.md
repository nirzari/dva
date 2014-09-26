dva
===

__dva's validation. again.__

Description
-----------
* `dva` is a tool to sanity-check instance images in cloud
* primary focus is RHEL release validation in [EC2](http://aws.amazon.com/documentation/ec2/)

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

Notes
-----
* please bare in mind the limit of opened file-descriptors is usualy 1024
* `--parallel-tests` and `--parallel-instances` multiply the usage of file-descriptors needed
* dva runs in a single process in [gevent](http://www.gevent.org/) pools
* consider running multiple `dva` instances for large inputs

See also
--------
* [valid](https://github.com/RedHatQE/valid)
