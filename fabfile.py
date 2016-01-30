# -*- coding: utf-8 -*-

from fabric.api import cd, run, local
from fabric.contrib.files import exists

code_path = "/root/www"
code_dir = "/root/www/myblog"
blog_dir = "myblog"


def init():
	with cd(code_path):
		run("git clone https://github.com/shenaishiren/myblog.git")


def remote_pull():
	with cd(code_dir):
		run("git pull")

def local_pull():
	local("git pull")


def prepare():
	env_dir = "env"
	with cd(code_dir):
		if not exists(env_dir):
			run("virtualenv env")
		run("env/bin/pip install --upgrade pip")
		run("env/bin/pip install -r requirements.txt")
		run("touch blog_error.log")
		run("touch blog_access.log")


def init_nginx():
	with cd(code_dir):
		run("mv blog.conf /etc/nginx/conf.d/")
		run("ln -s /etc/nginx/conf.d/blog.conf ./")


def deploy():
	with cd(code_dir):
		run("env/bin/python env/bin/gunicorn manage:app -c gunicorn_deploy.py")
		run("nginx -s reload")