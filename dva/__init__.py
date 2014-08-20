import sys
if 'threading' in sys.modules:
    print >>sys.stderr, '# Warning: expect an Un-handled KeyError at the exit of the program --- threading was imported before gevent!'
from gevent import monkey; monkey.patch_all()
from gevent import socket
socket.setdefaulttimeout(3)
