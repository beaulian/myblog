# -*- coding: utf-8 -*-
import os

SECRET_KEY = os.urandom(24)
PAGE_SIZE = 8
MONGO_AUTO_START_REQUEST = False
MONGO_DBNAME = "gavinblog"
DEBUG = True