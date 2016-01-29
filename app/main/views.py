# -*- coding: utf-8 -*-
from . import main
from app import mongo, bootstrap

from flask import render_template, request, flash, redirect, url_for
from flask.ext.paginate import Pagination
from flask_pymongo import DESCENDING
from flask_pymongo import ObjectId
from forms import BlogForm
from decorator import *
from config import *

@main.route("/", defaults={"page": 1}, methods=["GET"])
@main.route("/blog/page/<int:page>", methods=["GET"])
def index(page):
	page_size = PAGE_SIZE
	skip_num = (page -1) * page_size
	db_blogs = mongo.db.blogs.find()
	blog_collections = db_blogs.skip(skip_num) \
							   .limit(page_size) \
							   .sort("time", DESCENDING)
	blogs = list(blog_collections)
	pagination = Pagination(page=page, total=db_blogs.count(), per_page=page_size, bs_version='3')
	return render_template("index.html", blogs=blogs, pagination=pagination)


@main.route('/blog/<string:blog_id>', methods=["GET"])
def get_blog(blog_id):
	blog = mongo.db.Blogs.find_one_or_404({"_id": ObjectId(blog_id)})
	prev_blog = mongo.db.Blogs.find({"_id": {"$lt": ObjectId(blog_id)}}).limit(1)
	next_blog = mongo.db.Blogs.find({"_id": {"$gt": ObjectId(blog_id)}}).limit(1)
	mongo.db.blogs.update({'_id': ObjectId(blog_id)}, {'$inc': {'view_count': 1}})
	return render_template("blog.html", blog=blog, 
										prev_blog=prev_blog, 
										next_blog=next_blog)


@main.route("/postBlog", methods=["POST", "GET"])
def post_blog():
	form = BlogForm()
	if form.validate_on_submit():
		blog = form.get_blog()
		mongo.db.insert(blog)
		flash('发布成功')
		return redirect(request.args.get('next') or url_for('index'))
	return render_template('post.html', form=form)


@main.route("/editBlog/<string:blog_id>", methods=["GET", "POST"])
@login_required
def edit_blog(blog_id):
	blog = mongo.db.blogs.find_one_or_404({'_id': ObjectId(blog_id)})
	form = BlogForm(data=blog)
	if form.validate_on_submit():
		formdata = form.get_blog()
		formdata.pop("time")
		formdata.pop("view_count")
		mongo.db.blogs.update({"_id": ObjectId(blog_id)}, {"$set": data}, True, False)
		flash('更新成功')
		return redirect(request.args.get('next') or url_for('index'))
	return render_template('post.html', form=form)


@main.route("/deleteBlog/<string:blog_id>", methods=["GET", "POST"])
@login_required
def delete_blog(blog_id):
	mongo.db.blogs.remove({"_id": ObjectId(blog_id)})
	flash('删除成功')
	return redirect(request.args.get('next') or url_for('index')) 


