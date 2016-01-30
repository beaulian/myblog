# -*- coding: utf-8 -*-

from config import *


def allowed_file(filename):
    return '.' in filename and get_extension(filename) in ALLOWED_IMAGE_EXTENSIONS


def get_extension(filename):
	return filename.rsplit('.',1)[1]


def save_img(img_file):
	from PIL import Image
	from hashlib import md5
	from time import time

	im = Image.open(img_file)
	width, hight = im.getbbox()[2], im.getbbox()[3]
	if width > MAX_IMG_WIDTH:
		im = im.resize((MAX_IMG_WIDTH, hight * MAX_IMG_WIDTH / width), Image.ANTIALIAS)
		
	file_name = md5(str(time())).hexdigest() + "." + get_extension(img_file.filename)
	im.save(IMG_PATH + file_name)

	return SERVER_IMG_PATH + file_name
