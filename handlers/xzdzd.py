#!/usr/bin/env python
#coding=utf-8
import time
import random
import time
import tornado.web
import forms.xzdzd
import lib.utils

t_list = [x for x in range(1, 31)] + [y for y in range(32, 43) if y % 2 == 0] + [45, 48, 50, 55, 60]


class XzdzdHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(XzdzdHandler, self).__init__(*args, **kwargs)

    def get(self, template_varibles={"error": ""}):
        period = condition_type = None
        if 't' in self.request.arguments:
            t = self.request.arguments['t'][0]
            t = int(float(t) * 10)
            period = self.closest_t(t)
        if 'c' in self.request.arguments:
            c = int(self.request.arguments['c'][0])
            if c in [1, 2, 3, 4]:
                condition_type = c
        if period and condition_type:
            records = self.application.xzdzd_model.get_records(period, condition_type)
            records = sorted(records, key=lambda x: x["t_%s" % period], reverse=True)
            count = len(records)
            records = records[:count/2]
            for index, each in enumerate(records):
                each['rank'] = index + 1
            template_varibles = {"records": records, "count": count, "t": "t_%s" % period, "error": ""}
            self.render("xzdzd/xzdzd_result.html", **template_varibles)
            return
        self.render("xzdzd/xzdzd.html", **template_varibles)

    def post(self, *args, **kwargs):
        query_form = forms.xzdzd.XzdzdForm(self.request.arguments)
        if not query_form.validate():
            error = query_form.errors.items()[0][1][0]
            return self.get({"error": error})
        t = query_form.period.data
        c = query_form.type.data
        return self.redirect('/xzdzd?t=%s&c=%s' % (t, c))

    def closest_t(self, t):
        minimum = 100
        index = 0
        for each in t_list:
            if abs(t-each) <= minimum:
                minimum = abs(t-each)
                index = each
            else:
                return index