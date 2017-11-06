#!/usr/bin/python
#coding=utf8

from wtforms_tornado import Form
from wtforms import StringField, validators


class CreateForm(Form):
    title = StringField('title', [
        validators.DataRequired(message="文章标题不能为空"),
        validators.Length(max="50", message="文章标题过长"),
    ])
    content = StringField('content', [
        validators.DataRequired(message="内容不能为空"),
        validators.Length(max="20000", message="内容过长T_T")
    ])