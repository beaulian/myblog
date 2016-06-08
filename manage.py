# -*- coding: UTF-8 -*-

import os
os.popen("export PYTHONPATH=$(pwd)")

activate_this = 'env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from app import create_app
from flask.ext.script import Manager, Server

app = create_app()
manager = Manager(app)
server = Server(host='localhost', port=8000)
manager.add_command('server', server)

if __name__ == '__main__':
	manager.run()
