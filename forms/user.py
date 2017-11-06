#!/usr/bin/python
#coding=utf8

from wtforms_tornado import Form
from wtforms import StringField, validators


class LoginForm(Form):
    email = StringField('email', [validators.DataRequired(message="请填写邮箱地址"),
                                  validators.Email(message="请填入有效的邮箱地址"),
                                  validators.Length(min=4, message="请填入有效的邮箱地址")])
    password = StringField('password', [
        validators.DataRequired(message="请输入你的密码"),
        validators.Length(min=6, message="密码长度不对"),
        validators.Length(max=18, message="密码长度不对")
    ])


class RegisterForm(Form):
    username = StringField('username', [
        validators.DataRequired(message="必须填写用户名"),
        validators.Length(min=3, message="用户名长度必须大于3个字符"),
        validators.Length(max=10, message="用户名长度必须小于10个字符"),
        validators.Regexp("^[a-z][a-zA-Z0-9_]*$", message="用户名不得包含标点符号或汉字"),
    ])
    email = StringField('email', [validators.DataRequired(message="请填写邮箱地址"),
                                  validators.Email(message="请填入有效的邮箱地址"),
                                  validators.Length(min=4, message="请填入有效的邮箱地址")])
    password = StringField('password', [
        validators.DataRequired(message="请输入你的密码"),
        validators.Length(min=6, message="密码长度过短"),
        validators.Length(max=18, message="密码长度过长")
    ])

    password_confirm = StringField('confirm_password', [
        validators.EqualTo('password', message="两次输入的密码不一致")
    ])