# -*- coding: utf-8 -*-
import os

SECRET_KEY = "hard to guess"
PAGE_SIZE = 6
MONGO_AUTO_START_REQUEST = False
MONGO_DBNAME = "gavinblog"
#MONGO_MAX_POOL_SIZE = 200
#DEBUG = False
DEBUG = True
WTF_CSRF_ENABLED = False
IMG_PATH = os.getcwd() + "/app/static/img/"
SERVER_IMG_PATH = "/static/img/"
ALLOWED_IMAGE_EXTENSIONS = ['png','jpg','jpeg','gif']
MAX_IMG_WIDTH = 400
