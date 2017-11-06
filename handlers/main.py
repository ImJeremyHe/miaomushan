#!/usr/bin/env python
#coding=utf-8

import tornado.web
import forms.main
from base import BaseHandler


main_template_variables = {"notifications_count": 0}
create_template_variables = {"error": "", "title": "", "content": ""}


class MainHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(MainHandler, self).__init__(*args, **kwargs)
        self.rd_model = self.application.rd_main_model
        self.db = self.application.main_model

    def get(self, template_variables=main_template_variables):
        hot_tid = map(int, self.rd_model.get_hottest_tid(5))
        hot_essay_info = []
        for tid in hot_tid:
            hot_essay_info.append(self.db.get_essay_info_by_tid(tid)[0])
        template_variables["hot_essay"] = hot_essay_info
        self.render('blog/main.html', **template_variables)


class CreateHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(CreateHandler, self).__init__(*args, **kwargs)
        self.rd_model = self.application.rd_main_model

    @tornado.web.authenticated
    def get(self, template_variables=create_template_variables):
        self.render('blog/create.html', **template_variables)

    @tornado.web.authenticated
    def post(self, template_variables=create_template_variables):

        create_form = forms.main.CreateForm(self.request.arguments)
        form_title = getattr(create_form, "title", "").data
        form_content = getattr(create_form, "content", "").data
        if not create_form.validate():
            error = create_form.errors.items()[0][1][0]
            self.get({"title": form_title,
                      "content": form_content,
                      "error": error})
            return
        uid = self.current_user["uid"]
        username = self.current_user["username"]
        tid = self.application.main_model.create_essay(form_title, form_content, uid, username)
        print tid
        if tid:
            self.rd_model.add_hot_tid(tid, 0)
            self.redirect("/")
        else:
            self.get({"title": form_title, "content": form_content, "error": "哪里出了问题"})
            return


class ViewHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(ViewHandler, self).__init__(*args, **kwargs)
        self.main_model = self.application.main_model

    def get(self, tid, template_values={}):
        essay_info = self.main_model.get_essay_info_by_tid(tid)
        if essay_info:
            essay_info = essay_info[0]
            self.render('blog/view.html', essay_info=essay_info)
        else:
            self.render('snippet/404.html')
