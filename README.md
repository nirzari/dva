dva
===

__dva's validation. again.__

Installation
------------
* sudo python setup.py install
* or sudo pip install dva

Usage
-----
* dry-run: `dva validate -n < data.yaml > result.yaml`
* `dva validate < data.yaml > result.yaml`
* `dva bugzilla < result.yaml > buglist.yaml`
* `# dva result < result.yaml > result.txt`
* for complete options list: `dva --help`
* for failure summary use: `dva summary -i result.yaml`
* simulate valid execution: `dva validate -i data.yaml --parallel-tests=1 --sorted-mode`

See also
--------
* [valid](https://github.com/RedHatQE/valid)
