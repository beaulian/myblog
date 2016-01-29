# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.pymongo import PyMongo
from flask.ext.bootstrap import Bootstrap

import config

bootstrap = Bootstrap()
mongo = PyMongo()


def create_app():
	app = Flask(__name__)
	app.config.from_object('config')

	bootstrap.init_app(app)
	mongo.init_app(app)

	from main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app
