# -*- coding: utf-8 -*-
from . import main
from app import mongo, bootstrap

from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_pymongo import ObjectId
from forms import BlogForm
from decorator import *
from config import *
from models import *
from utils import *
import os

from werkzeug import secure_filename

@main.route("/", defaults={"page": 1}, methods=["GET"])
@main.route("/blog/page/<int:page>", methods=["GET"])
def index(page):
	blogs, pagination = get_blogs_pagination(page)
	return render_template("index.html", blogs=blogs, pagination=pagination)


@main.route('/blog/<string:blog_id>', methods=["GET"])
def get_blog(blog_id):
	blog = mongo.db.blogs.find_one_or_404({"_id": ObjectId(blog_id)})
	blog["class_name"] = blog["class_name"].split(";")
#	print blog["class_name"]
	prev_blog = get_prev_blog(blog_id)
	next_blog = get_next_blog(blog_id)
	mongo.db.blogs.update({'_id': ObjectId(blog_id)}, {'$inc': {'view_count': 1}})
	return render_template("blog.html", blog=blog, 
										prev_blog=prev_blog, 
										next_blog=next_blog)


@main.route("/postBlog", methods=["POST", "GET"])
@login_required
def post_blog():
	form = BlogForm()
	if form.validate_on_submit():
		blog = form.get_blog()
		mongo.db.blogs.insert(blog)
		flash('发布成功')
		return redirect(request.args.get('next') or url_for('main.index'))

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
		mongo.db.blogs.update({"_id": ObjectId(blog_id)}, {"$set": formdata}, True, False)
		flash('更新成功')
		return redirect(request.args.get('next') or url_for('main.index'))
	return render_template('post.html', form=form)


@main.route("/deleteBlog/<string:blog_id>", methods=["GET", "POST"])
@login_required
def delete_blog(blog_id):
	mongo.db.blogs.remove({"_id": ObjectId(blog_id)})
	flash('删除成功')
	return redirect(request.args.get('next') or url_for('main.index')) 


@main.route("/class/<string:class_name>", methods=["GET"])
def get_blog_by_class(class_name):
	page = request.args.get("page", 1)
	blogs, pagination = get_blogs_pagination(page, {"class_name": {"$regex": class_name}})
	return render_template('classes.html', blogs=blogs, pagination=pagination, class_name=class_name)


@main.route("/search", methods=["GET"])
def search_blog():
	page = request.args.get("page", 1)
	keyword = request.args.get("keyword", None)
	condition = {"$or": [
							{"title": {"$regex": keyword, "$options": "i"}},
							{"class_name": {"$regex": keyword, "$options": "i"}}
						]
				} if keyword else None
	blogs, pagination = get_blogs_pagination(page, condition)
	return render_template("index.html", blogs=blogs, pagination=pagination)


@main.route("/upload", methods=["POST"])
def upload():
	upload_file = request.files.get("upload_file", None)
	if upload_file:
		if allowed_file(upload_file.filename):
			file_path = save_img(upload_file)
			return jsonify({"success": True, "file_path": file_path})
		else:
			return jsonify({"success": False, "msg": "invalid file type"})
	else:
		return jsonify({"success": False, "msg": "please upload file"})



