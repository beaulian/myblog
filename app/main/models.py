# -*- coding: utf-8 -*-

from app import mongo
from flask_pymongo import ObjectId
from flask_pymongo import DESCENDING
from flask.ext.paginate import Pagination

from config import PAGE_SIZE

def get_prev_blog(blog_id):
	prev_blog = mongo.db.blogs.find({"_id": {"$lt": ObjectId(blog_id)}}).limit(1)
	if dict(prev_blog):
		prev_blog = dict(prev_blog)
		prev_blog["_id"] = str(prev_blog)
		return prev_blog
	return None


def get_next_blog(blog_id):
	next_blog = mongo.db.blogs.find({"_id": {"$gt": ObjectId(blog_id)}}).limit(1)
	if dict(next_blog):
		next_blog = dict(next_blog)
		next_blog["_id"] = str(next_blog["_id"])
		return next_blog
	return None


def get_blogs_pagination(page, condition=None):
	skip_num = (page -1) * PAGE_SIZE
	db_blogs = mongo.db.blogs.find(condition)
	blog_collections = db_blogs.skip(skip_num) \
							   .limit(PAGE_SIZE) \
							   .sort("time", DESCENDING)
	blogs = list(blog_collections)
	pagination = Pagination(page=page, total=db_blogs.count(), per_page=PAGE_SIZE, bs_version='3')
	return [blogs, pagination]
