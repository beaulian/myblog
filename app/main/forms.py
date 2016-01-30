#-*- coding: UTF-8 -*-
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, \
					BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length


class BlogForm(Form):
	title = StringField('title', validators=[DataRequired(), Length(1, 64)])
	body = TextAreaField('body', validators=[DataRequired()])
	class_name = StringField('class_name', validators=[DataRequired(), Length(1, 32)])
	submit = SubmitField('submit')

	def get_blog(self):
		blog_dict = {
			"title": self.title.data,
			"body": self.body.data,
			"class_name": self.class_name.data,
			"time": datetime.today().__format__("%Y-%m-%d %H:%M:%S"),
			"view_count": 0
		}
		return blog_dict