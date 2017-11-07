#!/usr/bin/env python
#coding=utf-8
import hashlib
import json
import time
import random
import time
import tornado.web
import forms.user
import lib.utils
from base import BaseHandler


register_template_varibles = dict(
    error=None,
    username="",
    password="",
    email="",
)

login_template_varibles = dict(
    error=None,
    email="",
    password="",
)


class LoginHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(LoginHandler, self).__init__(*args, **kwargs)

    def get(self, template_varibles=register_template_varibles):
        user_info = self.get_current_user()
        if user_info:
            self.redirect("/")
        else:
            self.render("user/login.html", **template_varibles)

    def post(self, template_varibles=login_template_varibles):
        login_form = forms.user.LoginForm(self.request.arguments)
        if not login_form.validate():
            error = login_form.errors.items()[0][1][0]
            email = getattr(login_form, "email", "").data
            return self.get({"error": error, "email": email})
        email = login_form.email.data
        password = hashlib.sha1(login_form.password.data).hexdigest()
        user_info = self.application.user_model.authenticate(email, password)
        if user_info:
            user_info = user_info[0]
            secret_key = str(int(round(time.time()) * 1000)) + hashlib.sha1(email).hexdigest()
            self.set_cookie("mms", secret_key)
            self.application.rd.set(secret_key, json.dumps(user_info, cls=lib.utils.MyEncoder))
            self.redirect("/")
        else:
            self.get({"error": "邮箱或密码不对", "email": email})


class RegisterHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(RegisterHandler, self).__init__(*args, **kwargs)

    def get(self, template_varibles=register_template_varibles):
        self.render("user/register.html", **template_varibles)

    def post(self, template_variables={}):
        template_variables = {}
        register_form = forms.user.RegisterForm(self.request.arguments)

        def get_inputted(e=""):
            _username = getattr(register_form, "username", "").data
            _password = getattr(register_form, "password", "").data
            _email = getattr(register_form, "email", "").data
            _template_variables = {
                "username": _username,
                "password": _password,
                "email": _email,
                "error": e,
            }
            return _template_variables
        if not register_form.validate():
            error = register_form.errors.items()[0][1][0]
            template_variables = get_inputted(error)
            self.get(template_variables)
            return
        username = register_form.username.data
        email = register_form.email.data

        duplicated_username = self.application.user_model.get_user_by("username", username)
        if duplicated_username:
            error = "该用户名已存在"
            self.get(get_inputted(error))
            return
        duplicated_email = self.application.user_model.get_user_by("email", email)
        if duplicated_email:
            error = "该邮箱已存在"
            self.get(get_inputted(error))
            return

        secure_password = hashlib.sha1(register_form.password.data).hexdigest()

        user_info = {"username": username,
                     "email": email,
                     "password": secure_password,
                     "created": time.strftime('%Y-%m-%d')}
        self.application.user_model.add_new_user(user_info)
        self.redirect(r'/login')


class LogoutHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(LogoutHandler, self).__init__(*args, **kwargs)

    @tornado.web.authenticated
    def get(self):
        self.user_info = {}
        key = self.get_secure_cookie("mms")
        self.application.rd.delete(key)
        self.redirect('/')
