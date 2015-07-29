import sys
from gevent import monkey; monkey.patch_all()
from gevent import socket

import dva.connection.gevent_ssl

socket.setdefaulttimeout(3)
