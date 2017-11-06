import tornado.web
import json


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.user_info = {}
        super(BaseHandler, self).__init__(*args, **kwargs)

    def get_current_user(self):
        if self.user_info:
            return self.user_info
        key = self.get_cookie("mms")
        if key:
            value = self.application.rd.get(key)
            if value:
                self.user_info = json.loads(value)
                return self.user_info
        return
