import sys, os
#sys.path.append( '/var/www/demoFlask')

from flup.server.fcgi import WSGIServer
from __init__ import app

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    WSGIServer(app, bindAddress=("/tmp/site-kernotek.sock")).run()







