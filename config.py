# -*- coding: utf-8 -*-
import os

SECRET_KEY = os.urandom(24)
PAGE_SIZE = 8
MONGO_AUTO_START_REQUEST = False
MONGO_DBNAME = "gavinblog"
DEBUG = False
# DEBUG = True
WTF_CSRF_ENABLED = False
IMG_PATH = os.getcwd() + "/app/static/img/"
SERVER_IMG_PATH = "/static/img/"
ALLOWED_IMAGE_EXTENSIONS = ['png','jpg','jpeg','gif']
MAX_IMG_WIDTH = 400
