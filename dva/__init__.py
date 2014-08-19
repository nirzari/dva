from gevent import monkey; monkey.patch_all(thread=False)
from gevent import socket
socket.setdefaulttimeout(3)
